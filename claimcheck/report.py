"""Build local JSON + Markdown reports from a stored run (and compare runs)."""
from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

from . import config
from .data import load_answers, load_gold


def _fmt(x: Any) -> str:
    if x is None:
        return "null"
    if isinstance(x, float):
        return f"{x:.4f}"
    return str(x)


def enrich_development(run: dict[str, Any]) -> dict[str, Any]:
    """Harness-side diagnostics joined from gold AFTER predictions were saved."""
    gold = {g.claim_id: g for g in load_gold(answers=load_answers())}
    diag = run.get("diagnostics") or {}
    preds = {c["claim_id"]: c for a in run["answers"] for c in a["claims"]}
    status = {a["answer_id"]: a for a in run["answers"]}

    missed = []
    for gid in diag.get("missed_gold_ids", []):
        g = gold[gid]
        missed.append({"gold_claim_id": gid, "expected_label": g.expected_label, "quote": g.quote,
                       "difficulty_tags": list(g.difficulty_tags),
                       "answer_status": status[g.answer_id]["status"],
                       "answer_error_type": status[g.answer_id]["error_type"]})
    extra = []
    for pid in diag.get("unmatched_prediction_ids", []):
        p = preds[pid]
        overlapping = [g.claim_id for g in gold.values() if g.answer_id == pid.split(":")[0]
                       and g.start_char < p["end_char"] and p["start_char"] < g.end_char]
        extra.append({"claim_id": pid, "label": p["label"], "quote": p["quote"],
                      "overlaps_gold_ids": overlapping})
    wrong = []
    for w in diag.get("wrong_label_ids", []):
        g = gold[w["claim_id"]]
        p = preds.get(w["claim_id"], {})
        wrong.append({"claim_id": w["claim_id"], "predicted": w["predicted"], "expected": w["expected"],
                      "quote": g.quote, "gold_explanation": g.explanation,
                      "difficulty_tags": list(g.difficulty_tags), "predicted_reason": p.get("reason"),
                      "predicted_fact_ids": p.get("fact_ids"), "gold_fact_ids": list(g.evidence_fact_ids)})

    # Per-tag and confusion breakdowns (gold claims in scheduled answers).
    scheduled = {a["answer_id"] for a in run["answers"]}
    by_tag: dict[str, Counter] = defaultdict(Counter)
    confusion: Counter = Counter()
    for g in gold.values():
        if g.answer_id not in scheduled:
            continue
        p = preds.get(g.claim_id)
        outcome = "missed" if p is None else ("correct" if p["label"] == g.expected_label else "wrong_label")
        confusion[(g.expected_label, p["label"] if p else "missed")] += 1
        for t in g.difficulty_tags:
            by_tag[t][outcome] += 1
            by_tag[t]["total"] += 1
    return {
        "missed": missed,
        "extra": extra,
        "wrong_label": wrong,
        "by_tag": {t: dict(c) for t, c in sorted(by_tag.items(), key=lambda kv: -kv[1]["total"])},
        "confusion": [{"expected": e, "predicted": p, "n": n} for (e, p), n in sorted(confusion.items())],
    }


def build_report(run: dict[str, Any]) -> dict[str, Any]:
    rep = {k: run[k] for k in ("run_id", "status", "split", "agent_version", "prompt_version", "prompt_sha256",
                               "dataset_version", "evaluator_version", "fact_version", "provider", "model",
                               "settings", "source_revision", "file_hashes", "created_at", "finished_at",
                               "counts", "scores", "failure_reason")}
    rep["answers"] = run["answers"]
    if run["split"] == "development" and run["status"] == "completed":
        rep["diagnostics"] = run.get("diagnostics")
        rep["analysis"] = enrich_development(run)
    else:
        rep["diagnostics"] = None
        rep["analysis"] = None
        rep["note"] = ("Check split: the candidate has no gold labels. G, M, C, matches, expected labels and all "
                       "quality metrics are intentionally null; the reviewer scores the saved predictions.")
        # A check-split claim must never carry match information.
        for a in rep["answers"]:
            for c in a["claims"]:
                for k in ("gold_match", "gold_claim_id", "expected_label", "label_correct"):
                    c[k] = None
    return rep


def render_markdown(rep: dict[str, Any]) -> str:
    L: list[str] = []
    L.append(f"# Run report: {rep['agent_version']} / {rep['split']}")
    L.append("")
    L.append(f"- run_id: `{rep['run_id']}`  status: **{rep['status']}**")
    L.append(f"- provider/model: `{rep['provider']}` / `{rep['model']}`")
    L.append(f"- prompt: `{rep['prompt_version']}` sha256 `{rep['prompt_sha256'][:16]}…`")
    L.append(f"- dataset `{rep['dataset_version']}`, facts `{rep['fact_version']}`, evaluator `{rep['evaluator_version']}`")
    L.append(f"- source revision: `{rep['source_revision']}`")
    L.append(f"- started {rep['created_at']}, finished {rep['finished_at']}")
    L.append(f"- settings: `{json.dumps(rep['settings'])}`")
    L.append(f"- file hashes: `{json.dumps(rep['file_hashes'])}`")
    L.append("")
    c = rep["counts"] or {}
    L.append("## Counts")
    L.append("")
    L.append("| scheduled | ok | errors | empty ok | P | G | M | C | latency total (s) | tokens in/out |")
    L.append("|---|---|---|---|---|---|---|---|---|---|")
    L.append(f"| {c.get('scheduled_answers')} | {c.get('ok_answers')} | {c.get('error_answers')} | "
             f"{c.get('empty_ok_answers')} | {c.get('P')} | {_fmt(c.get('G'))} | {_fmt(c.get('M'))} | "
             f"{_fmt(c.get('C'))} | {round((c.get('total_latency_ms') or 0) / 1000, 1)} | "
             f"{c.get('input_tokens')}/{c.get('output_tokens')} |")
    if c.get("answer_error_types"):
        L.append("")
        L.append(f"Answer error types: `{json.dumps(c['answer_error_types'])}`")
    L.append("")
    L.append("## Metrics")
    L.append("")
    s = rep["scores"]
    if s is None:
        L.append(rep.get("note") or "Metrics are null for this run.")
    else:
        L.append("| | precision | recall | F1 |")
        L.append("|---|---|---|---|")
        L.append(f"| extraction | {_fmt(s['extraction_precision'])} | {_fmt(s['extraction_recall'])} | {_fmt(s['extraction_f1'])} |")
        L.append(f"| joint (span + label) | {_fmt(s['joint_precision'])} | {_fmt(s['joint_recall'])} | **{_fmt(s['joint_f1'])}** |")
        L.append("")
        L.append(f"Gold claim coverage C/G: {_fmt((rep.get('diagnostics') or {}).get('gold_claim_coverage'))}")
    an = rep.get("analysis")
    if an:
        L.append("")
        L.append("## Label confusion (rows = expected)")
        L.append("")
        labels = ["supported", "contradicted", "unknown", "missed"]
        grid = {(x["expected"], x["predicted"]): x["n"] for x in an["confusion"]}
        L.append("| expected \\ predicted | " + " | ".join(labels) + " |")
        L.append("|---" * (len(labels) + 1) + "|")
        for e in labels[:3]:
            L.append(f"| {e} | " + " | ".join(str(grid.get((e, p), 0)) for p in labels) + " |")
        L.append("")
        L.append("## By difficulty tag")
        L.append("")
        L.append("| tag | total | correct | wrong label | missed |")
        L.append("|---|---|---|---|---|")
        for t, d in an["by_tag"].items():
            L.append(f"| {t} | {d.get('total', 0)} | {d.get('correct', 0)} | {d.get('wrong_label', 0)} | {d.get('missed', 0)} |")
        L.append("")
        L.append(f"## Missed gold claims ({len(an['missed'])})")
        L.append("")
        for m in an["missed"]:
            note = f" (answer error: {m['answer_error_type']})" if m["answer_status"] == "error" else ""
            L.append(f"- `{m['gold_claim_id']}` [{m['expected_label']}; {', '.join(m['difficulty_tags'])}]{note}: {m['quote']}")
        L.append("")
        L.append(f"## Extra / unmatched predictions ({len(an['extra'])})")
        L.append("")
        for x in an["extra"]:
            ov = f" (overlaps {', '.join(x['overlaps_gold_ids'])})" if x["overlaps_gold_ids"] else ""
            L.append(f"- `{x['claim_id']}` [{x['label']}]{ov}: {x['quote']}")
        L.append("")
        L.append(f"## Matched but wrong label ({len(an['wrong_label'])})")
        L.append("")
        for w in an["wrong_label"]:
            L.append(f"- `{w['claim_id']}` predicted **{w['predicted']}**, expected **{w['expected']}** "
                     f"[{', '.join(w['difficulty_tags'])}]: {w['quote']}")
            L.append(f"  - model reason: {w['predicted_reason']}  (facts {w['predicted_fact_ids']})")
            L.append(f"  - gold: {w['gold_explanation']}  (facts {w['gold_fact_ids']})")
    L.append("")
    L.append("## Answer outcomes and predictions")
    for a in rep["answers"]:
        L.append("")
        err = f" — {a['error_type']}: {a['error_message']}" if a["status"] == "error" else ""
        L.append(f"### {a['answer_id']}: {a['status']}{err}")
        L.append(f"turns={a['turns']} latency={a['latency_ms']}ms claims={a['n_claims']} trace=`{a['trace_ref']}`")
        L.append("")
        for cl in a["claims"]:
            m = ""
            if cl.get("gold_match") is not None:
                m = " ✓span" if cl["gold_match"] else " ✗span"
                if cl.get("label_correct") is not None:
                    m += " ✓label" if cl["label_correct"] else f" ✗label(expected {cl['expected_label']})"
            L.append(f"- `{cl['claim_id']}` **{cl['label']}**{m} {cl['fact_ids']}: {cl['quote']}")
            L.append(f"  - {cl['reason']}")
    return "\n".join(L) + "\n"


def write_report(run: dict[str, Any], name: str | None = None) -> tuple[Path, Path]:
    rep = build_report(run)
    name = name or f"{rep['agent_version']}_{rep['split']}"
    config.REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    jp = config.REPORTS_DIR / f"{name}.json"
    mp = config.REPORTS_DIR / f"{name}.md"
    jp.write_text(json.dumps(rep, ensure_ascii=False, indent=2, default=str), encoding="utf-8")
    mp.write_text(render_markdown(rep), encoding="utf-8")
    return jp, mp


def compare_runs(runs: list[dict[str, Any]]) -> str:
    """Markdown table comparing stored runs plus v1->v2 development flips."""
    L = ["# Four-run comparison", "",
         "| run | split | status | ok/err | P | G | M | C | ext P | ext R | ext F1 | joint P | joint R | joint F1 | coverage C/G |",
         "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for r in runs:
        c, s = r["counts"] or {}, r["scores"] or {}
        cov = (r.get("diagnostics") or {}).get("gold_claim_coverage")
        L.append(f"| {r['agent_version']} `{r['run_id'][:8]}` | {r['split']} | {r['status']} | "
                 f"{c.get('ok_answers')}/{c.get('error_answers')} | {c.get('P')} | {_fmt(c.get('G'))} | "
                 f"{_fmt(c.get('M'))} | {_fmt(c.get('C'))} | {_fmt(s.get('extraction_precision'))} | "
                 f"{_fmt(s.get('extraction_recall'))} | {_fmt(s.get('extraction_f1'))} | "
                 f"{_fmt(s.get('joint_precision'))} | {_fmt(s.get('joint_recall'))} | "
                 f"**{_fmt(s.get('joint_f1'))}** | {_fmt(cov)} |")
    dev = {r["agent_version"]: r for r in runs if r["split"] == "development" and r["status"] == "completed"}
    if "v1" in dev and "v2" in dev:
        def outcome_map(run):
            out = {}
            preds = {c["claim_id"]: c for a in run["answers"] for c in a["claims"]}
            for g in load_gold():
                p = preds.get(g.claim_id)
                out[g.claim_id] = ("missed" if p is None else ("correct" if p["label"] == g.expected_label
                                                               else f"wrong:{p['label']}"), g)
            extras = {cid for cid, c in preds.items() if c.get("gold_match") is False}
            return out, extras
        o1, x1 = outcome_map(dev["v1"])
        o2, x2 = outcome_map(dev["v2"])
        fixed = [k for k in o1 if o1[k][0] != "correct" and o2[k][0] == "correct"]
        broke = [k for k in o1 if o1[k][0] == "correct" and o2[k][0] != "correct"]
        L += ["", "## Development v1 → v2 per-claim changes", "",
              f"- gold claims fixed by v2 (not correct in v1, correct in v2): **{len(fixed)}**",
              f"- regressions (correct in v1, not correct in v2): **{len(broke)}**",
              f"- extra predictions: v1 {len(x1)}, v2 {len(x2)} (new in v2: {len(x2 - x1)}, removed: {len(x1 - x2)})", ""]
        for title, ids in (("Fixed", fixed), ("Regressed", broke)):
            L.append(f"### {title}")
            L.append("")
            for k in ids:
                g = o1[k][1]
                L.append(f"- `{k}` expected {g.expected_label} [{', '.join(g.difficulty_tags)}]: "
                         f"v1 {o1[k][0]} → v2 {o2[k][0]}")
            L.append("")
    return "\n".join(L) + "\n"
