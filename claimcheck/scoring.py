"""Deterministic scorer: exact span matching, extraction and joint P/R/F1.

Definitions over the whole labelled split:
  G = gold claims, P = accepted predictions,
  M = exact span matches (answer_id, start_char, end_char) regardless of label,
  C = matches whose label is also correct.
  extraction P = M/P, R = M/G, F1 = 2M/(P+G)
  joint      P = C/P, R = C/G, F1 = 2C/(P+G)
A zero denominator gives 0 when the split has gold claims. Check splits (no
gold available to the candidate) get null quality metrics. No fuzzy matching,
no LLM judge. Answer errors contribute no predictions but keep all their gold
claims in G as missed.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from .data import GoldClaim


class ScoringInputError(ValueError):
    pass


@dataclass(frozen=True)
class PredClaim:
    answer_id: str
    claim_id: str
    start_char: int
    end_char: int
    quote: str
    label: str


@dataclass(frozen=True)
class AnswerOutcome:
    answer_id: str
    status: str  # "ok" | "error"
    error_type: str | None = None


def _div(n: int, d: int) -> float:
    return n / d if d else 0.0


def check_outcomes(scheduled_ids: Iterable[str], outcomes: Iterable[AnswerOutcome]) -> dict[str, AnswerOutcome]:
    scheduled = list(scheduled_ids)
    by_id: dict[str, AnswerOutcome] = {}
    for o in outcomes:
        if o.answer_id in by_id:
            raise ScoringInputError(f"duplicate answer outcome for {o.answer_id}")
        if o.status not in ("ok", "error"):
            raise ScoringInputError(f"bad outcome status {o.status!r} for {o.answer_id}")
        by_id[o.answer_id] = o
    missing = [a for a in scheduled if a not in by_id]
    if missing:
        raise ScoringInputError(f"missing answer outcomes: {missing}")
    extra = [a for a in by_id if a not in set(scheduled)]
    if extra:
        raise ScoringInputError(f"outcomes for unscheduled answers: {extra}")
    return by_id


def score_split(
    split: str,
    scheduled_ids: list[str],
    outcomes: list[AnswerOutcome],
    predictions: list[PredClaim],
    gold: list[GoldClaim] | None,
    answer_texts: dict[str, str] | None = None,
) -> dict:
    by_id = check_outcomes(scheduled_ids, outcomes)
    scheduled = set(scheduled_ids)

    # Predictions may only come from successful answers.
    for p in predictions:
        if p.answer_id not in scheduled:
            raise ScoringInputError(f"prediction for unscheduled answer {p.answer_id}")
        if by_id[p.answer_id].status != "ok":
            raise ScoringInputError(f"prediction attached to errored answer {p.answer_id}")
        # Validate quote equality before matching.
        if answer_texts is not None and answer_texts[p.answer_id][p.start_char:p.end_char] != p.quote:
            raise ScoringInputError(f"prediction {p.claim_id} quote does not equal its span")
    keys = [(p.answer_id, p.start_char, p.end_char) for p in predictions]
    if len(keys) != len(set(keys)):
        raise ScoringInputError("duplicate predicted spans")

    counts = {
        "scheduled_answers": len(scheduled_ids),
        "ok_answers": sum(1 for o in by_id.values() if o.status == "ok"),
        "error_answers": sum(1 for o in by_id.values() if o.status == "error"),
        "empty_ok_answers": sum(
            1 for a, o in by_id.items() if o.status == "ok" and not any(p.answer_id == a for p in predictions)),
        "P": len(predictions),
        "G": None, "M": None, "C": None,
    }
    error_types: dict[str, int] = {}
    for o in by_id.values():
        if o.status == "error":
            error_types[o.error_type or "unspecified"] = error_types.get(o.error_type or "unspecified", 0) + 1

    if gold is None:  # check split: quality is computed by the reviewer only
        return {
            "split": split,
            "counts": counts,
            "answer_error_types": error_types,
            "metrics": None,
            "gold_claim_coverage": None,
            "missed_gold_ids": None,
            "unmatched_prediction_ids": None,
            "wrong_label_ids": None,
            "per_claim": None,
        }

    gold_in_split = [g for g in gold if g.answer_id in scheduled]
    gold_by_key = {(g.answer_id, g.start_char, g.end_char): g for g in gold_in_split}
    if len(gold_by_key) != len(gold_in_split):
        raise ScoringInputError("duplicate gold spans")

    G, P = len(gold_in_split), len(predictions)
    matched_gold: set[str] = set()
    unmatched_pred: list[str] = []
    wrong_label: list[dict] = []
    per_claim: dict[str, dict] = {}
    C = 0
    for p in predictions:
        g = gold_by_key.get((p.answer_id, p.start_char, p.end_char))
        if g is None or g.claim_id in matched_gold:
            unmatched_pred.append(p.claim_id)
            per_claim[p.claim_id] = {"gold_match": False, "gold_claim_id": None,
                                     "expected_label": None, "label_correct": None}
            continue
        matched_gold.add(g.claim_id)
        ok = p.label == g.expected_label
        C += int(ok)
        per_claim[p.claim_id] = {"gold_match": True, "gold_claim_id": g.claim_id,
                                 "expected_label": g.expected_label, "label_correct": ok}
        if not ok:
            wrong_label.append({"claim_id": g.claim_id, "predicted": p.label, "expected": g.expected_label})
    M = len(matched_gold)
    missed = [g.claim_id for g in gold_in_split if g.claim_id not in matched_gold]

    has_gold = G > 0
    if not scheduled_ids:
        metrics = None
    else:
        metrics = {
            "extraction_precision": _div(M, P) if has_gold else None,
            "extraction_recall": _div(M, G) if has_gold else None,
            "extraction_f1": _div(2 * M, P + G) if has_gold else None,
            "joint_precision": _div(C, P) if has_gold else None,
            "joint_recall": _div(C, G) if has_gold else None,
            "joint_f1": _div(2 * C, P + G) if has_gold else None,
        }
    counts.update({"G": G, "M": M, "C": C})
    return {
        "split": split,
        "counts": counts,
        "answer_error_types": error_types,
        "metrics": metrics,
        "gold_claim_coverage": _div(C, G) if has_gold else None,
        "missed_gold_ids": missed,
        "unmatched_prediction_ids": unmatched_pred,
        "wrong_label_ids": wrong_label,
        "per_claim": per_claim,
    }
