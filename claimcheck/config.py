"""Runtime settings and fixed version identifiers.

Everything that must stay identical between v1 and v2 runs (provider, model,
timeout, turn limit, token budget, data and evaluator versions) lives here so a
run records exactly what it used.
"""
from __future__ import annotations

import os
from dataclasses import asdict, dataclass, field
from pathlib import Path

from dotenv import load_dotenv

REPO_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = REPO_ROOT / "data"
REPORTS_DIR = REPO_ROOT / "reports"
TRACES_DIR = REPO_ROOT / "traces"
PROMPTS_DIR = Path(__file__).resolve().parent / "prompts"

ANSWERS_CSV = DATA_DIR / "answers.csv"
FACTS_CSV = DATA_DIR / "brand_facts.csv"
GOLD_CSV = DATA_DIR / "development_gold.csv"

DATASET_VERSION = "long-brand-answers-50-v4"
FACT_VERSION = "speaker-catalogue-v4"
EVALUATOR_VERSION = "sentence-spans-and-labels-v4"
SCORER_IMPL_VERSION = "claimcheck-scorer-1"

AGENT_VERSIONS = ("v1", "v2")
SPLITS = ("development", "check")
LABELS = ("supported", "contradicted", "unknown")

# Loaded once at import so both the CLI and the API see the same values.
load_dotenv(REPO_ROOT / ".env", override=False)


@dataclass(frozen=True)
class Settings:
    provider: str = "anthropic"
    model: str = "claude-sonnet-5-5"
    # The harness environment may export its own ANTHROPIC_BASE_URL; we use a
    # separate variable so the public API is always the default target.
    api_base: str = "https://api.anthropic.com"
    request_timeout_s: float = 180.0
    max_turns: int = 3
    max_tokens: int = 16000
    # The SDK/model used here rejects `temperature`, so sampling is the
    # provider default. Recorded so reports state it explicitly.
    sampling: str = "provider-default (temperature not accepted by model)"
    sdk_max_retries: int = 0
    extra: dict = field(default_factory=dict)

    def public_dict(self) -> dict:
        d = asdict(self)
        d.pop("extra", None)
        return d


def load_settings() -> Settings:
    return Settings(
        model=os.getenv("CLAIMCHECK_MODEL", Settings.model),
        api_base=os.getenv("CLAIMCHECK_API_BASE", Settings.api_base),
        request_timeout_s=float(os.getenv("CLAIMCHECK_TIMEOUT_S", Settings.request_timeout_s)),
        max_turns=int(os.getenv("CLAIMCHECK_MAX_TURNS", Settings.max_turns)),
        max_tokens=int(os.getenv("CLAIMCHECK_MAX_TOKENS", Settings.max_tokens)),
    )


def api_key() -> str | None:
    return os.getenv("ANTHROPIC_API_KEY")


def database_url() -> str | None:
    return os.getenv("DATABASE_URL")
