import json

import pytest

from claimcheck.agent import build_user_message, run_agent
from claimcheck.providers.base import ProviderError, ProviderTimeout
from claimcheck.providers.fake import FakeProvider, text_response, tool_call_response
from claimcheck.schemas import AgentInput

from .helpers import gold_claims_for, lookup, perfect_provider


def inp(a):
    return AgentInput(answer_id=a.answer_id, brand_id=a.brand_id, question=a.question, ai_answer=a.ai_answer)


@pytest.fixture
def a01(answers):
    return answers["A01"]


def run(a, steps, store, settings, version="v1"):
    prov = FakeProvider(steps)
    return run_agent(inp(a), version, prov, store, settings), prov


def test_happy_path_offsets_from_python(a01, gold, store, settings):
    prov = perfect_provider(gold, a01)
    res = run_agent(inp(a01), "v1", prov, store, settings)
    assert res.status == "ok" and res.turns == 2
    expected = [(g.start_char, g.end_char) for g in gold if g.answer_id == "A01"]
    assert [(c.start_char, c.end_char) for c in res.output.claims] == expected
    for c in res.output.claims:
        assert a01.ai_answer[c.start_char:c.end_char] == c.quote
        assert c.claim_id == f"A01:{c.start_char}:{c.end_char}"


def test_multiple_tool_calls_in_one_turn(a01, gold, store, settings):
    steps = [tool_call_response(("get_brand_facts", {"brand_id": "cleartrail"}),
                                ("get_brand_facts", {"brand_id": "stonewave"})),
             text_response({"answer_id": "A01", "claims": gold_claims_for(gold, "A01")})]
    res, prov = run(a01, steps, store, settings)
    assert res.status == "ok"
    tool_msg = prov.calls[1]["messages"][-1]["content"]
    assert [json.loads(t["content"])["brand_id"] for t in tool_msg] == ["cleartrail", "stonewave"]
    assert all(json.loads(t["content"])["fact_version"] == "speaker-catalogue-v4" for t in tool_msg)


@pytest.mark.parametrize("final,etype", [
    ("I think these are fine.", "malformed_output"),
    ({"answer_id": "A01", "claims": [{"quote": "x.", "label": "mostly_true", "fact_ids": [], "reason": "r"}]},
     "schema_violation"),
    ({"answer_id": "A01", "claims": [{"quote": "This sentence is not in the answer.", "label": "unknown",
                                       "fact_ids": [], "reason": "r"}]}, "quote_not_found"),
])
def test_malformed_and_unsupported_outputs(a01, store, settings, final, etype):
    res, _ = run(a01, [lookup(), text_response(final)], store, settings)
    assert res.status == "error" and res.error_type == etype and res.output is None


def test_invented_fact_id_is_answer_error(a01, gold, store, settings):
    claims = gold_claims_for(gold, "A01")
    claims[0]["fact_ids"] = ["cleartrail.mini.amplifier_watts"]
    res, _ = run(a01, [lookup(), text_response({"answer_id": "A01", "claims": claims})], store, settings)
    assert res.status == "error" and res.error_type == "invalid_fact_id" and res.output is None


def test_fact_id_from_brand_not_looked_up_is_error(a01, gold, store, settings):
    claims = gold_claims_for(gold, "A01")
    claims[0]["fact_ids"] = ["stonewave.go.weight"]
    res, _ = run(a01, [lookup("cleartrail"), text_response({"answer_id": "A01", "claims": claims})], store, settings)
    assert res.error_type == "ungrounded_fact_id"


def test_illegal_tool_is_not_executed(a01, store, settings):
    res, prov = run(a01, [tool_call_response(("run_shell", {"cmd": "rm -rf /"}))], store, settings)
    assert res.status == "error" and res.error_type == "illegal_tool"
    assert len(prov.calls) == 1  # nothing executed, no further turns


def test_unknown_requested_brand(a01, store, settings):
    res, _ = run(a01, [tool_call_response(("get_brand_facts", {"brand_id": "acmesound"}))], store, settings)
    assert res.error_type == "unknown_requested_brand"


@pytest.mark.parametrize("args", [{}, {"brand_id": 3}, {"brand_id": "cleartrail", "extra": 1}, "cleartrail"])
def test_invalid_tool_arguments(a01, store, settings, args):
    res, _ = run(a01, [tool_call_response(("get_brand_facts", args))], store, settings)
    assert res.error_type == "invalid_tool_arguments"


def test_unknown_primary_brand(store, settings):
    bad = AgentInput(answer_id="Z1", brand_id="acmesound", question="q", ai_answer="Text.")
    res = run_agent(bad, "v1", FakeProvider([]), store, settings)
    assert res.error_type == "unknown_primary_brand" and res.turns == 0


def test_timeout_and_provider_error(a01, store, settings):
    res, _ = run(a01, [lookup(), ProviderTimeout("provider request exceeded 5s timeout")], store, settings)
    assert res.status == "error" and res.error_type == "provider_timeout" and res.output is None
    res, _ = run(a01, [ProviderError("provider returned HTTP 529 (OverloadedError)")], store, settings)
    assert res.error_type == "provider_error"


def test_turn_limit_exhaustion(a01, store, settings):
    res, prov = run(a01, [lookup(), lookup(), lookup(), lookup()], store, settings)
    assert res.status == "error" and res.error_type == "turn_limit_exhausted"
    assert len(prov.calls) == 3 and res.turns == 3


def test_final_answer_without_tool_use_is_error(a01, store, settings):
    res, _ = run(a01, [text_response({"answer_id": "A01", "claims": []})], store, settings)
    assert res.error_type == "no_tool_use"


def test_truncated_output_is_error(a01, store, settings):
    res, _ = run(a01, [lookup(), text_response('{"answer_id": "A01", "claims": [', stop_reason="max_tokens")],
                 store, settings)
    assert res.error_type == "truncated_output"


def test_valid_empty_claims(a01, store, settings):
    res, _ = run(a01, [lookup(), text_response({"answer_id": "A01", "claims": []})], store, settings)
    assert res.status == "ok" and res.output.claims == []


def test_gold_never_enters_model_or_tool_payloads(answers, gold, store, settings):
    for aid in ("A01", "A07", "A23"):
        a = answers[aid]
        prov = perfect_provider(gold, a)
        run_agent(inp(a), "v1", prov, store, settings)
        blob = json.dumps(prov.calls, ensure_ascii=False)
        for g in gold:
            assert g.claim_id not in blob
            assert g.explanation not in blob
        # Gold field names as JSON keys (the bare word "explanation" occurs in some answer texts).
        for forbidden in ("expected_label", "evidence_fact_ids", "difficulty_tags", "explanation",
                          "start_char", "end_char", "claim_id"):
            assert f'"{forbidden}":' not in blob
        assert "development_gold" not in blob
        # The model sees exactly the four agent input fields.
        first_user = prov.calls[0]["messages"][0]["content"]
        assert first_user == build_user_message(inp(a))
        record = json.loads(first_user.split("<answer_record>\n", 1)[1].rsplit("\n</answer_record>", 1)[0])
        assert set(record) == {"answer_id", "brand_id", "question", "ai_answer"}


def test_agent_input_rejects_gold_fields():
    with pytest.raises(Exception):
        AgentInput(answer_id="A", brand_id="b", question="q", ai_answer="t", claims=[])
