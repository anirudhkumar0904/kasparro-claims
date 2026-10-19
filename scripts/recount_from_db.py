"""Independent recount of development metrics straight from PostgreSQL rows.

Deliberately does NOT import claimcheck.scoring: it re-implements exact span
matching with the csv module so the stored scores can be cross-checked.

  python scripts/recount_from_db.py <run_id> [<run_id> ...]
"""
import csv
import os
import sys
from pathlib import Path

import psycopg
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent.parent
load_dotenv(ROOT / ".env")


def main(run_ids):
    with open(ROOT / "data" / "development_gold.csv", encoding="utf-8", newline="") as fh:
        gold = list(csv.DictReader(fh))
    with open(ROOT / "data" / "answers.csv", encoding="utf-8", newline="") as fh:
        texts = {r["answer_id"]: r["ai_answer"] for r in csv.DictReader(fh)}
    with psycopg.connect(os.environ["DATABASE_URL"]) as conn:
        for rid in run_ids:
            split, scores = conn.execute("SELECT split, scores FROM runs WHERE run_id = %s", (rid,)).fetchone()
            if split != "development":
                print(rid, split, "-> no gold for this split; skipped")
                continue
            sched = {r[0] for r in conn.execute("SELECT answer_id FROM answer_results WHERE run_id = %s", (rid,))}
            rows = conn.execute("SELECT answer_id, start_char, end_char, quote, label FROM claim_results "
                                "WHERE run_id = %s", (rid,)).fetchall()
            gk = {(g["answer_id"], int(g["start_char"]), int(g["end_char"])): g["expected_label"]
                  for g in gold if g["answer_id"] in sched}
            assert all(texts[a][s:e] == q for a, s, e, q, _ in rows), "stored quote != slice"
            G, P = len(gk), len(rows)
            M = sum((a, s, e) in gk for a, s, e, _, _ in rows)
            C = sum(gk.get((a, s, e)) == lab for a, s, e, _, lab in rows)
            mine = {"extraction_f1": 2 * M / (P + G) if P + G else 0.0, "joint_f1": 2 * C / (P + G) if P + G else 0.0}
            same = all(abs(mine[k] - scores[k]) < 1e-12 for k in mine)
            print(f"{rid} G={G} P={P} M={M} C={C} ext_F1={mine['extraction_f1']:.4f} "
                  f"joint_F1={mine['joint_f1']:.4f} matches_stored={same}")


if __name__ == "__main__":
    main(sys.argv[1:])
