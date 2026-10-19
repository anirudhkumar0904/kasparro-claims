"""Sequential evaluation runner shared by the CLI and POST /evaluation-runs.

Order of operations guarantees gold never reaches inference:
  1. create the run row (status=running) with all versions, settings, hashes
  2. for each scheduled answer: run the agent on AgentInput only, write the
     sanitized trace, persist the terminal answer row + accepted claims
  3. only after every prediction is saved, load gold (development only),
     score, and annotate claim rows with the optional match
  4. mark the run completed (answer errors allowed) or failed (infrastructure)
"""
from __future__ import annotations

import json
import subprocess
import uuid
from typing import Any, Callable

from . import config
from .agent import AgentResult, prompt_sha256, run_agent
from .config import Settings
from .data import answers_for_split, file_hashes, load_answers, load_gold
from .db import Database
from .facts_tool import FactStore
from .providers.base import Provider
from .schemas import AgentInput
from .scoring import AnswerOutcome, PredClaim, score_split

ProviderFactory = Callable[[str], Provider]


def source_revision() -> str | None:
    try:
        rev = subprocess.run(["git", "rev-parse", "HEAD"], cwd=config.REPO_ROOT, capture_output=True,
                             text=True, timeout=5)
        if rev.returncode != 0:
            return None
        dirty = subprocess.run(["git", "status", "--porcelain", "--", "claimcheck"], cwd=config.REPO_ROOT,
                               capture_output=True, text=True, timeout=5).stdout.strip()
        return rev.stdout.strip() + ("-dirty" if dirty else "")
    except Exception:
        return None


def run_metadata(version: str, split: str, provider_name: str, model: str, settings: Settings) -> dict[str, Any]:
    return {
        "split": split,
        "agent_version": version,
        "prompt_version": f"prompts/{version}.md",
        "prompt_sha256": prompt_sha256(version),
        "dataset_version": config.DATASET_VERSION,
        "evaluator_version": f"{config.EVALUATOR_VERSION} ({config.SCORER_IMPL_VERSION})",
        "fact_version": config.FACT_VERSION,
        "provider": provider_name,
        "model": model,
        "settings": settings.public_dict(),
        "source_revision": source_revision(),
        "file_hashes": file_hashes(),
    }


def _write_trace(run_id: uuid.UUID, result: AgentResult) -> str:
    out_dir = config.TRACES_DIR / str(run_id)
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / f"{result.answer_id}.json"
    path.write_text(json.dumps(result.trace, ensure_ascii=False, indent=2), encoding="utf-8")
    return str(path.relative_to(config.REPO_ROOT))


def run_evaluation(version: str, split: str, provider_factory: ProviderFactory, provider_name: str,
                   model: str, db: Database, settings: Settings, store: FactStore | None = None,
                   progress: Callable[[str], None] | None = None) -> dict[str, Any]:
    store = store or FactStore()
    answers = answers_for_split(split)
    meta = run_metadata(version, split, provider_name, model, settings)
    run_id = db.create_run(meta)
    outcomes: list[AnswerOutcome] = []
    preds: list[PredClaim] = []
    counts: dict[str, Any] = {"scheduled_answers": len(answers), "processed_answers": 0}
    latencies: list[int] = []
    tokens_in: list[int] = []
    tokens_out: list[int] = []
    try:
        for i, a in enumerate(answers):
            inp = AgentInput(answer_id=a.answer_id, brand_id=a.brand_id, question=a.question, ai_answer=a.ai_answer)
            result = run_agent(inp, version, provider_factory(a.answer_id), store, settings)
            trace_ref = _write_trace(run_id, result)
            claims = [c.model_dump() for c in result.output.claims] if result.output else []
            db.save_answer_result(run_id, i, {
                "answer_id": a.answer_id,
                "status": result.status,
                "error_type": result.error_type,
                "error_message": result.error_message,
                "latency_ms": result.latency_ms,
                "turns": result.turns,
                "input_tokens": result.usage.get("input_tokens"),
                "output_tokens": result.usage.get("output_tokens"),
                "trace_ref": trace_ref,
            }, claims)
            outcomes.append(AnswerOutcome(a.answer_id, result.status, result.error_type))
            preds.extend(PredClaim(a.answer_id, c["claim_id"], c["start_char"], c["end_char"], c["quote"], c["label"])
                         for c in claims)
            latencies.append(result.latency_ms)
            tokens_in.append(int(result.usage.get("input_tokens", 0)))
            tokens_out.append(int(result.usage.get("output_tokens", 0)))
            counts["processed_answers"] = i + 1
            if progress:
                progress(f"[{i + 1}/{len(answers)}] {a.answer_id} {result.status}"
                         f"{' ' + str(result.error_type) if result.error_type else ''} "
                         f"claims={len(claims)} {result.latency_ms}ms")

        # --- predictions are all persisted; only now may gold be joined ---
        gold = load_gold(answers=load_answers()) if split == "development" else None
        score = score_split(split, [a.answer_id for a in answers], outcomes, preds, gold,
                            answer_texts={a.answer_id: a.ai_answer for a in answers})
        if score["per_claim"]:
            db.apply_gold_matches(run_id, score["per_claim"])
        diagnostics = None
        if split == "development":
            diagnostics = {
                "missed_gold_ids": score["missed_gold_ids"],
                "unmatched_prediction_ids": score["unmatched_prediction_ids"],
                "wrong_label_ids": score["wrong_label_ids"],
                "gold_claim_coverage": score["gold_claim_coverage"],
            }
        final_counts = {**score["counts"], "processed_answers": counts["processed_answers"],
                        "answer_error_types": score["answer_error_types"],
                        "total_latency_ms": sum(latencies),
                        "input_tokens": sum(tokens_in), "output_tokens": sum(tokens_out)}
        db.finish_run(run_id, "completed", final_counts, score["metrics"], diagnostics)
        return {"run_id": str(run_id), "status": "completed", "counts": final_counts,
                "metrics": score["metrics"], "diagnostics": diagnostics}
    except BaseException as exc:  # interrupted or infrastructure failure: keep partial evidence
        counts["ok_answers"] = sum(1 for o in outcomes if o.status == "ok")
        counts["error_answers"] = sum(1 for o in outcomes if o.status == "error")
        counts["P"] = len(preds)
        try:
            db.finish_run(run_id, "failed", counts, None, None, f"{type(exc).__name__}")
        finally:
            if not isinstance(exc, Exception):
                raise
        return {"run_id": str(run_id), "status": "failed", "counts": counts, "metrics": None,
                "diagnostics": None, "failure_reason": type(exc).__name__}
