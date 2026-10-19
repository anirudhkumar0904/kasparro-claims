import pytest

from claimcheck.schemas import Claim, RawClaim, RawOutput
from claimcheck.validation import (OutputValidationError, build_output, clamp_reason, locate_quotes,
                                   parse_model_json, validate_claims)

TEXT = "Alpha is 5 kg. Buy it now. Alpha is 5 kg. Beta has Wi-Fi."


def claim(aid, s, e, text=TEXT, label="unknown", fact_ids=(), reason="r."):
    return Claim(claim_id=f"{aid}:{s}:{e}", start_char=s, end_char=e, quote=text[s:e], label=label,
                 fact_ids=list(fact_ids), reason=reason)


def test_locate_resolves_repeated_quotes_in_document_order():
    spans = locate_quotes(TEXT, ["Alpha is 5 kg.", "Alpha is 5 kg.", "Beta has Wi-Fi."])
    assert spans == [(0, 14), (27, 41), (42, 57)]
    assert [TEXT[s:e] for s, e in spans] == ["Alpha is 5 kg.", "Alpha is 5 kg.", "Beta has Wi-Fi."]


def test_locate_rejects_missing_whitespace_and_overcount():
    with pytest.raises(OutputValidationError) as e:
        locate_quotes(TEXT, ["Gamma is new."])
    assert e.value.error_type == "quote_not_found"
    with pytest.raises(OutputValidationError) as e:
        locate_quotes(TEXT, [" Alpha is 5 kg."])
    assert e.value.error_type == "invalid_span"
    with pytest.raises(OutputValidationError) as e:
        locate_quotes(TEXT, ["Beta has Wi-Fi.", "Beta has Wi-Fi."])
    assert e.value.error_type == "duplicate_claim"


def test_valid_offsets_pass(store):
    out = validate_claims("X", TEXT, [claim("X", 0, 14), claim("X", 42, 57)], store)
    assert [c.claim_id for c in out.claims] == ["X:0:14", "X:42:57"]


@pytest.mark.parametrize("claims,etype", [
    ([Claim(claim_id="X:0:999", start_char=0, end_char=999, quote="x", label="unknown", fact_ids=[], reason="r")], "invalid_span"),
    ([Claim(claim_id="X:0:14", start_char=0, end_char=14, quote="Alpha is 6 kg.", label="unknown", fact_ids=[], reason="r")], "quote_mismatch"),
    ([Claim(claim_id="X:0:15", start_char=0, end_char=15, quote=TEXT[0:15], label="unknown", fact_ids=[], reason="r")], "invalid_span"),
    ([Claim(claim_id="Y:0:14", start_char=0, end_char=14, quote=TEXT[0:14], label="unknown", fact_ids=[], reason="r")], "invalid_claim_id"),
    ([claim("X", 0, 14), claim("X", 0, 14)], "duplicate_claim"),
    ([claim("X", 0, 14), claim("X", 9, 26)], "overlapping_claims"),
    ([claim("X", 42, 57), claim("X", 0, 14)], "unordered_claims"),
    ([claim("X", 0, 14, fact_ids=["cleartrail.mini.invented"])], "invalid_fact_id"),
])
def test_invalid_claim_lists_are_rejected(store, claims, etype):
    with pytest.raises(OutputValidationError) as e:
        validate_claims("X", TEXT, claims, store)
    assert e.value.error_type == etype


def test_fact_ids_must_come_from_looked_up_brands(store):
    c = claim("X", 0, 14, fact_ids=["stonewave.go.weight"])
    validate_claims("X", TEXT, [c], store, allowed_brands={"stonewave"})
    with pytest.raises(OutputValidationError) as e:
        validate_claims("X", TEXT, [c], store, allowed_brands={"cleartrail"})
    assert e.value.error_type == "ungrounded_fact_id"


def test_build_output_assigns_ids_and_sorts(store):
    raw = RawOutput(answer_id="X", claims=[
        RawClaim(quote="Beta has Wi-Fi.", label="unknown", fact_ids=[], reason="No row."),
        RawClaim(quote="Alpha is 5 kg.", label="unknown", fact_ids=[], reason="No row."),
    ])
    out = build_output("X", TEXT, raw, store, set())
    assert [c.claim_id for c in out.claims] == ["X:0:14", "X:42:57"]
    with pytest.raises(OutputValidationError) as e:
        build_output("Z", TEXT, raw, store, set())
    assert e.value.error_type == "answer_id_mismatch"


def test_parse_model_json_errors():
    with pytest.raises(OutputValidationError) as e:
        parse_model_json("Here are the claims: [")
    assert e.value.error_type == "malformed_output"
    with pytest.raises(OutputValidationError) as e:
        parse_model_json('{"answer_id": "X", "claims": [{"quote": "a.", "label": "true", "fact_ids": [], "reason": "r"}]}')
    assert e.value.error_type == "schema_violation"
    with pytest.raises(OutputValidationError) as e:
        parse_model_json('{"answer_id": "X", "claims": [], "start_char": 3}')
    assert e.value.error_type == "schema_violation"
    assert parse_model_json('```json\n{"answer_id": "X", "claims": []}\n```').claims == []


def test_reason_is_clamped_to_two_sentences():
    assert clamp_reason("One. Two. Three.") == "One. Two."
    assert clamp_reason("Version 5.3 matches.") == "Version 5.3 matches."
