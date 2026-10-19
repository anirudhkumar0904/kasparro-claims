"""CSV loading with exact text preservation and typed fact values.

Rules from the brief that this module enforces:
* parse with the csv module (quoted commas / embedded newlines are data),
* decode as UTF-8 and never strip, normalise or resave ai_answer,
* booleans are the literal text "true"/"false" (never bool("false")),
* blank unit / condition mean "not applicable" (stored as None).
"""
from __future__ import annotations

import csv
import hashlib
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Any

from . import config

ANSWER_FIELDS = ["answer_id", "split", "brand_id", "question", "ai_answer"]
FACT_FIELDS = ["fact_id", "brand_id", "model_id", "field", "value", "value_type",
               "unit", "condition", "valid_from", "valid_to"]
GOLD_FIELDS = ["answer_id", "claim_id", "start_char", "end_char", "quote",
               "expected_label", "evidence_fact_ids", "explanation", "difficulty_tags"]


class DataError(ValueError):
    pass


def _read_rows(path: Path, expected_fields: list[str]) -> list[dict[str, str]]:
    # newline="" is required so the csv module sees embedded line breaks
    # inside quoted fields exactly as written.
    with open(path, encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        if reader.fieldnames != expected_fields:
            raise DataError(f"{path.name}: unexpected header {reader.fieldnames}")
        rows = list(reader)
    for i, row in enumerate(rows):
        if None in row or any(v is None for v in row.values()):
            raise DataError(f"{path.name}: malformed row {i + 2}")
    return rows


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def file_hashes() -> dict[str, str]:
    return {p.name: sha256_file(p) for p in (config.ANSWERS_CSV, config.FACTS_CSV, config.GOLD_CSV)}


# ---------------------------------------------------------------- answers
@dataclass(frozen=True)
class Answer:
    answer_id: str
    split: str
    brand_id: str
    question: str
    ai_answer: str


def load_answers(path: Path = config.ANSWERS_CSV) -> list[Answer]:
    rows = _read_rows(path, ANSWER_FIELDS)
    answers = [Answer(**row) for row in rows]
    ids = [a.answer_id for a in answers]
    if len(ids) != len(set(ids)):
        raise DataError("duplicate answer_id in answers.csv")
    for a in answers:
        if a.split not in config.SPLITS:
            raise DataError(f"{a.answer_id}: unknown split {a.split!r}")
    return answers


def answers_for_split(split: str, path: Path = config.ANSWERS_CSV) -> list[Answer]:
    if split not in config.SPLITS:
        raise DataError(f"unknown split {split!r}")
    return [a for a in load_answers(path) if a.split == split]


# ---------------------------------------------------------------- facts
def parse_bool(text: str) -> bool:
    if text == "true":
        return True
    if text == "false":
        return False
    raise DataError(f"boolean value must be 'true' or 'false', got {text!r}")


def parse_typed_value(text: str, value_type: str) -> Any:
    if value_type == "boolean":
        return parse_bool(text)
    if value_type == "number":
        try:
            num = float(text)
        except ValueError as exc:
            raise DataError(f"bad number {text!r}") from exc
        return int(num) if num.is_integer() and "." not in text else num
    if value_type == "string":
        return text
    raise DataError(f"unknown value_type {value_type!r}")


@dataclass(frozen=True)
class Fact:
    fact_id: str
    brand_id: str
    model_id: str
    field: str
    value: Any
    value_type: str
    unit: str | None
    condition: str | None
    valid_from: date | None
    valid_to: date | None

    def as_tool_row(self) -> dict[str, Any]:
        """JSON-safe representation returned to the model by the tool."""
        return {
            "fact_id": self.fact_id,
            "brand_id": self.brand_id,
            "model_id": self.model_id,
            "field": self.field,
            "value": self.value,
            "value_type": self.value_type,
            "unit": self.unit,
            "condition": self.condition,
            "valid_from": self.valid_from.isoformat() if self.valid_from else None,
            "valid_to": self.valid_to.isoformat() if self.valid_to else None,
        }


def _parse_date(text: str) -> date | None:
    if text == "":
        return None
    try:
        return date.fromisoformat(text)
    except ValueError as exc:
        raise DataError(f"date must be YYYY-MM-DD, got {text!r}") from exc


def load_facts(path: Path = config.FACTS_CSV) -> list[Fact]:
    facts = []
    for row in _read_rows(path, FACT_FIELDS):
        facts.append(Fact(
            fact_id=row["fact_id"],
            brand_id=row["brand_id"],
            model_id=row["model_id"],
            field=row["field"],
            value=parse_typed_value(row["value"], row["value_type"]),
            value_type=row["value_type"],
            unit=row["unit"] or None,
            condition=row["condition"] or None,
            valid_from=_parse_date(row["valid_from"]),
            valid_to=_parse_date(row["valid_to"]),
        ))
    ids = [f.fact_id for f in facts]
    if len(ids) != len(set(ids)):
        raise DataError("duplicate fact_id in brand_facts.csv")
    return facts


# ---------------------------------------------------------------- gold (harness only)
@dataclass(frozen=True)
class GoldClaim:
    answer_id: str
    claim_id: str
    start_char: int
    end_char: int
    quote: str
    expected_label: str
    evidence_fact_ids: tuple[str, ...]
    explanation: str
    difficulty_tags: tuple[str, ...]


def load_gold(path: Path = config.GOLD_CSV, answers: list[Answer] | None = None) -> list[GoldClaim]:
    """Load development gold. Used only by the scorer, never by the agent."""
    gold = []
    for row in _read_rows(path, GOLD_FIELDS):
        gold.append(GoldClaim(
            answer_id=row["answer_id"],
            claim_id=row["claim_id"],
            start_char=int(row["start_char"]),
            end_char=int(row["end_char"]),
            quote=row["quote"],
            expected_label=row["expected_label"],
            evidence_fact_ids=tuple(x for x in row["evidence_fact_ids"].split("|") if x),
            explanation=row["explanation"],
            difficulty_tags=tuple(x for x in row["difficulty_tags"].split("|") if x),
        ))
    if answers is not None:
        by_id = {a.answer_id: a for a in answers}
        for g in gold:
            a = by_id.get(g.answer_id)
            if a is None or a.ai_answer[g.start_char:g.end_char] != g.quote:
                raise DataError(f"gold span {g.claim_id} does not match ai_answer")
    return gold
