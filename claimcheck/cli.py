"""Command line entry points.

  python -m claimcheck.cli init-db
  python -m claimcheck.cli run --agent-version v1 --split development [--report-name v1_development]
  python -m claimcheck.cli report <run_id> [--name v1_development]
  python -m claimcheck.cli compare <run_id> <run_id> ...
"""
from __future__ import annotations

import argparse
import sys
import uuid

from . import config
from .db import Database
from .providers import live_provider_factory
from .report import compare_runs, write_report
from .runner import run_evaluation


def _db() -> Database:
    url = config.database_url()
    if not url:
        sys.exit("DATABASE_URL is not set (see .env.example)")
    db = Database(url)
    db.init_schema()
    return db


def main(argv: list[str] | None = None) -> None:
    ap = argparse.ArgumentParser(prog="claimcheck")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("init-db")
    r = sub.add_parser("run")
    r.add_argument("--agent-version", choices=config.AGENT_VERSIONS, required=True)
    r.add_argument("--split", choices=config.SPLITS, required=True)
    r.add_argument("--report-name")
    rp = sub.add_parser("report")
    rp.add_argument("run_id")
    rp.add_argument("--name")
    cp = sub.add_parser("compare")
    cp.add_argument("run_ids", nargs="+")
    cp.add_argument("--out", default=str(config.REPORTS_DIR / "comparison.md"))
    args = ap.parse_args(argv)

    if args.cmd == "init-db":
        _db()
        print("schema ready")
    elif args.cmd == "run":
        db = _db()
        settings = config.load_settings()
        factory = live_provider_factory(settings)
        summary = run_evaluation(args.agent_version, args.split, factory, factory.name,
                                 factory.model, db, settings, progress=lambda m: print(m, flush=True))
        print(summary["run_id"], summary["status"], summary["counts"], summary["metrics"])
        run = db.get_run(uuid.UUID(summary["run_id"]))
        jp, mp = write_report(run, args.report_name)
        print(f"report: {jp} {mp}")
    elif args.cmd == "report":
        db = _db()
        run = db.get_run(uuid.UUID(args.run_id))
        if run is None:
            sys.exit("run not found")
        print(*write_report(run, args.name))
    elif args.cmd == "compare":
        db = _db()
        runs = [db.get_run(uuid.UUID(x)) for x in args.run_ids]
        if any(r is None for r in runs):
            sys.exit("run not found")
        md = compare_runs(runs)
        with open(args.out, "w", encoding="utf-8") as fh:
            fh.write(md)
        print(md)


if __name__ == "__main__":
    main()
