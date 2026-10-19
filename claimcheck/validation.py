"""Turn the model's quoted claims into validated, offset-bearing claims.

The model never counts characters. It returns verbatim sentence quotes; this
module locates each quote in the exact ai_answer string and then validates the
whole claim list. Any violation raises OutputValidationError, which the agent
turns into an answer-level error with zero accepted predictions.
"""
from __future__ import annotations

import json
import re
from typing import Iterable

from pydantic import ValidationError

from . import config
from .facts_tool import FactStore
from .schemas import AgentOutput, Claim, RawOutput

MAX_REASON_SENTENCES = 2


class OutputValidationError(ValueError):
    def __init__(self, error_type: str, message: str):
        super().__init__(message)
        self.error_type = error_type
        self.message = message


def parse_model_json(text: str) -> RawOutput:
    """Parse the final assistant text as the RawOutput JSON object."""
    stripped = text.strip()
    fence = re.fullmatch(r"```(?:json)?\s*(.*?)\s*```", stripped, re.S)
    if fence:
        stripped = fence.group(1)
    try:
        obj = json.loads(stripped)
    except json.JSONDecodeError as exc:
        raise OutputValidationError("malformed_output", f"final output is not valid JSON: {exc.msg}") from exc
    try:
        return RawOutput.model_validate(obj)
    except ValidationError as exc:
        first = exc.errors()[0]
        loc = ".".join(str(p) for p in first.get("loc", ()))
        raise OutputValidationError("schema_violation", f"{loc}: {first.get('msg')}") from exc


def _split_sentences(reason: str) -> list[str]:
    return [p for p in re.split(r"(?<=[.!?])\s+", reason.strip()) if p]


def _count_sentences(reason: str) -> int:
    return len(_split_sentences(reason))


def clamp_reason(reason: str) -> str:
    """Keep at most two sentences. The reason is free text, not one of the
    validated fields (spans, labels, fact IDs), so it is trimmed rather than
    failing the whole answer."""
    parts = _split_sentences(reason)
    return " ".join(parts[:MAX_REASON_SENTENCES])


def locate_quotes(ai_answer: str, quotes: Iterable[str]) -> list[tuple[int, int]]:
    """Return (start, end) for each quote, in input order.

    Repeated identical text is resolved from document order: the model lists
    claims in reading order, so each quote takes the first occurrence that
    starts at or after the previous claim's end; if none, the first unused one.
    """
    spans: list[tuple[int, int]] = []
    used: set[int] = set()
    cursor = 0
    for q in quotes:
        if q != q.strip():
            raise OutputValidationError("invalid_span", "quote has leading or trailing whitespace")
        occurrences = [m.start() for m in re.finditer(re.escape(q), ai_answer)]
        if not occurrences:
            raise OutputValidationError("quote_not_found", f"quote not found verbatim in ai_answer: {q[:80]!r}")
        free = [o for o in occurrences if o not in used]
        if not free:
            raise OutputValidationError("duplicate_claim", f"quote repeated more times than it occurs: {q[:80]!r}")
        after = [o for o in free if o >= cursor]
        start = after[0] if after else free[0]
        used.add(start)
        end = start + len(q)
        spans.append((start, end))
        cursor = max(cursor, end)
    return spans


def validate_claims(answer_id: str, ai_answer: str, claims: list[Claim], store: FactStore,
                    allowed_brands: set[str] | None = None) -> AgentOutput:
    """Full structural validation of a final claim list (also used on
    already-offset claims, e.g. in tests and the scorer's input check)."""
    seen_ids: set[str] = set()
    prev_end = -1
    prev_start = -1
    for c in claims:
        if not (0 <= c.start_char < c.end_char <= len(ai_answer)):
            raise OutputValidationError("invalid_span", f"span {c.start_char}:{c.end_char} out of bounds")
        if ai_answer[c.start_char:c.end_char] != c.quote:
            raise OutputValidationError("quote_mismatch", f"quote does not equal ai_answer[{c.start_char}:{c.end_char}]")
        if c.quote != c.quote.strip() or not c.quote:
            raise OutputValidationError("invalid_span", "quote has leading/trailing whitespace or is empty")
        expected_id = f"{answer_id}:{c.start_char}:{c.end_char}"
        if c.claim_id != expected_id:
            raise OutputValidationError("invalid_claim_id", f"claim_id {c.claim_id!r} != {expected_id!r}")
        if c.claim_id in seen_ids:
            raise OutputValidationError("duplicate_claim", f"duplicate claim_id {c.claim_id}")
        seen_ids.add(c.claim_id)
        if c.start_char < prev_start:
            raise OutputValidationError("unordered_claims", "claims are not in increasing start_char order")
        if c.start_char < prev_end:
            raise OutputValidationError("overlapping_claims", f"claim {c.claim_id} overlaps the previous claim")
        prev_start, prev_end = c.start_char, c.end_char
        if c.label not in config.LABELS:
            raise OutputValidationError("invalid_label", f"label {c.label!r}")
        if len(set(c.fact_ids)) != len(c.fact_ids):
            raise OutputValidationError("invalid_fact_id", f"duplicate fact_id in {c.claim_id}")
        for fid in c.fact_ids:
            fact = store.fact(fid)
            if fact is None:
                raise OutputValidationError("invalid_fact_id", f"fact_id {fid!r} does not exist")
            if allowed_brands is not None and fact.brand_id not in allowed_brands:
                raise OutputValidationError(
                    "ungrounded_fact_id", f"fact_id {fid!r} belongs to a brand that was not looked up")
        if _count_sentences(c.reason) > MAX_REASON_SENTENCES:
            raise OutputValidationError("invalid_reason", f"reason for {c.claim_id} exceeds two sentences")
    return AgentOutput(answer_id=answer_id, claims=claims)


def build_output(answer_id: str, ai_answer: str, raw: RawOutput, store: FactStore,
                 allowed_brands: set[str]) -> AgentOutput:
    if raw.answer_id != answer_id:
        raise OutputValidationError("answer_id_mismatch", "model returned a different answer_id")
    spans = locate_quotes(ai_answer, [rc.quote for rc in raw.claims])
    claims = [
        Claim(
            claim_id=f"{answer_id}:{s}:{e}",
            start_char=s,
            end_char=e,
            quote=ai_answer[s:e],
            label=rc.label,
            fact_ids=list(rc.fact_ids),
            reason=clamp_reason(rc.reason),
        )
        for rc, (s, e) in zip(raw.claims, spans)
    ]
    claims.sort(key=lambda c: c.start_char)
    return validate_claims(answer_id, ai_answer, claims, store, allowed_brands)
