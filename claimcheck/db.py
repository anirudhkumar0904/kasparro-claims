"""PostgreSQL persistence with parameterized SQL (psycopg 3, no ORM)."""
from __future__ import annotations

import uuid
from pathlib import Path
from typing import Any

import psycopg
from psycopg.rows import dict_row
from psycopg.types.json import Jsonb

SCHEMA_PATH = Path(__file__).resolve().parent / "schema.sql"


class Database:
    def __init__(self, url: str):
        if not url:
            raise RuntimeError("DATABASE_URL is not configured")
        self.url = url

    def connect(self) -> psycopg.Connection:
        return psycopg.connect(self.url, row_factory=dict_row)

    def init_schema(self) -> None:
        with self.connect() as conn:
            conn.execute(SCHEMA_PATH.read_text(encoding="utf-8"))

    # ------------------------------------------------------------- writes
    def create_run(self, meta: dict[str, Any]) -> uuid.UUID:
        run_id = uuid.uuid4()
        with self.connect() as conn:
            conn.execute(
                """
                INSERT INTO runs (run_id, status, split, agent_version, prompt_version, prompt_sha256,
                                  dataset_version, evaluator_version, fact_version, provider, model,
                                  settings, source_revision, file_hashes)
                VALUES (%s, 'running', %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """,
                (run_id, meta["split"], meta["agent_version"], meta["prompt_version"], meta["prompt_sha256"],
                 meta["dataset_version"], meta["evaluator_version"], meta["fact_version"], meta["provider"],
                 meta["model"], Jsonb(meta["settings"]), meta.get("source_revision"), Jsonb(meta["file_hashes"])),
            )
        return run_id

    def save_answer_result(self, run_id: uuid.UUID, ordinal: int, res: dict[str, Any],
                           claims: list[dict[str, Any]]) -> None:
        """One transaction per answer: the terminal answer row plus its accepted claims."""
        with self.connect() as conn, conn.transaction():
            conn.execute(
                """
                INSERT INTO answer_results (run_id, answer_id, ordinal, status, error_type, error_message,
                                            latency_ms, turns, input_tokens, output_tokens, n_claims, trace_ref)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """,
                (run_id, res["answer_id"], ordinal, res["status"], res.get("error_type"), res.get("error_message"),
                 res["latency_ms"], res["turns"], res.get("input_tokens"), res.get("output_tokens"),
                 len(claims), res.get("trace_ref")),
            )
            for c in claims:
                conn.execute(
                    """
                    INSERT INTO claim_results (run_id, answer_id, claim_id, start_char, end_char, quote,
                                               label, fact_ids, reason)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """,
                    (run_id, res["answer_id"], c["claim_id"], c["start_char"], c["end_char"], c["quote"],
                     c["label"], Jsonb(c["fact_ids"]), c["reason"]),
                )

    def apply_gold_matches(self, run_id: uuid.UUID, per_claim: dict[str, dict]) -> None:
        with self.connect() as conn, conn.transaction():
            for claim_id, m in per_claim.items():
                conn.execute(
                    """
                    UPDATE claim_results
                       SET gold_match = %s, gold_claim_id = %s, expected_label = %s, label_correct = %s
                     WHERE run_id = %s AND claim_id = %s
                    """,
                    (m["gold_match"], m["gold_claim_id"], m["expected_label"], m["label_correct"],
                     run_id, claim_id),
                )

    def finish_run(self, run_id: uuid.UUID, status: str, counts: dict | None, scores: dict | None,
                   diagnostics: dict | None, failure_reason: str | None = None) -> None:
        with self.connect() as conn:
            conn.execute(
                """
                UPDATE runs SET status = %s, finished_at = now(), counts = %s, scores = %s,
                                diagnostics = %s, failure_reason = %s
                 WHERE run_id = %s
                """,
                (status, Jsonb(counts) if counts is not None else None,
                 Jsonb(scores) if scores is not None else None,
                 Jsonb(diagnostics) if diagnostics is not None else None, failure_reason, run_id),
            )

    # ------------------------------------------------------------- reads
    def get_run(self, run_id: uuid.UUID) -> dict[str, Any] | None:
        with self.connect() as conn:
            run = conn.execute("SELECT * FROM runs WHERE run_id = %s", (run_id,)).fetchone()
            if run is None:
                return None
            rows = conn.execute(
                """
                SELECT a.answer_id, a.ordinal, a.status, a.error_type, a.error_message, a.latency_ms,
                       a.turns, a.input_tokens, a.output_tokens, a.n_claims, a.trace_ref,
                       c.claim_id, c.start_char, c.end_char, c.quote, c.label, c.fact_ids, c.reason,
                       c.gold_match, c.gold_claim_id, c.expected_label, c.label_correct
                  FROM answer_results a
             LEFT JOIN claim_results c ON c.run_id = a.run_id AND c.answer_id = a.answer_id
                 WHERE a.run_id = %s
              ORDER BY a.ordinal, a.answer_id, c.start_char NULLS FIRST, c.end_char
                """,
                (run_id,),
            ).fetchall()
        answers: list[dict[str, Any]] = []
        index: dict[str, dict[str, Any]] = {}
        for r in rows:
            a = index.get(r["answer_id"])
            if a is None:
                a = {k: r[k] for k in ("answer_id", "status", "error_type", "error_message", "latency_ms",
                                       "turns", "input_tokens", "output_tokens", "n_claims", "trace_ref")}
                a["claims"] = []
                index[r["answer_id"]] = a
                answers.append(a)
            if r["claim_id"] is not None:
                a["claims"].append({k: r[k] for k in (
                    "claim_id", "start_char", "end_char", "quote", "label", "fact_ids", "reason",
                    "gold_match", "gold_claim_id", "expected_label", "label_correct")})
        run["run_id"] = str(run["run_id"])
        for k in ("created_at", "finished_at"):
            if run.get(k) is not None:
                run[k] = run[k].isoformat()
        run["answers"] = answers
        return run
