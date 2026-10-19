"""Shared builders for fake-provider scripts."""
from claimcheck.providers.fake import FakeProvider, text_response, tool_call_response


def gold_claims_for(gold, answer_id, label_override=None):
    return [{"quote": g.quote, "label": label_override or g.expected_label,
             "fact_ids": list(g.evidence_fact_ids), "reason": "Matches the catalogue."}
            for g in gold if g.answer_id == answer_id]


def brands_for(gold, answer):
    b = {f.split(".")[0] for g in gold if g.answer_id == answer.answer_id for f in g.evidence_fact_ids}
    return sorted(b | {answer.brand_id})


def perfect_script(gold, answer):
    return [tool_call_response(*[("get_brand_facts", {"brand_id": b}) for b in brands_for(gold, answer)]),
            text_response({"answer_id": answer.answer_id, "claims": gold_claims_for(gold, answer.answer_id)})]


def perfect_provider(gold, answer):
    return FakeProvider(perfect_script(gold, answer))


def lookup(brand="cleartrail"):
    return tool_call_response(("get_brand_facts", {"brand_id": brand}))
