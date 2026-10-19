import uuid

import psycopg
import pytest
from fastapi.testclient import TestClient

from claimcheck import api
from claimcheck.providers import ProviderFactory
from claimcheck.providers.base import ProviderError, ProviderTimeout
from claimcheck.providers.fake import FakeProvider, ScriptedByAnswer, text_response
from claimcheck.runner import run_evaluation

from .helpers import lookup, perfect_script


@pytest.fixture
def client_with(db, store, settings):
    def make(factory):
        api.app.dependency_overrides[api.get_db] = lambda: db
        api.app.dependency_overrides[api.get_store] = lambda: store
        api.app.dependency_overrides[api.get_settings] = lambda: settings
        api.app.dependency_overrides[api.get_provider_factory] = lambda: factory
        return TestClient(api.app)
    yield make
    api.app.dependency_overrides.clear()


def body(a, **extra):
    return {"answer_id": a.answer_id, "brand_id": a.brand_id, "question": a.question,
            "ai_answer": a.ai_answer, "agent_version": "v1", **extra}


def single(steps):
    return ProviderFactory(lambda _aid: FakeProvider(list(steps)), "fake", "fake-model")


# ------------------------------------------------------------------ /classify
def test_classify_200(client_with, answers, gold):
    a = answers["A01"]
    c = client_with(single(perfect_script(gold, a)))
    r = c.post("/classify", json=body(a))
    assert r.status_code == 200
    data = r.json()
    assert data["answer_id"] == "A01" and len(data["claims"]) == 9
    assert [x["start_char"] for x in data["claims"]] == sorted(x["start_char"] for x in data["claims"])


@pytest.mark.parametrize("mutate", [
    lambda b: b.update(claims=[{"quote": "x"}]),
    lambda b: b.update(gold_spans=[[0, 10]]),
    lambda b: b.update(expected_label="supported"),
    lambda b: b.pop("ai_answer"),
    lambda b: b.update(agent_version="v3"),
    lambda b: b.update(answer_id=""),
])
def test_classify_422(client_with, answers, mutate):
    c = client_with(single([]))
    b = body(answers["A01"])
    mutate(b)
    r = c.post("/classify", json=b)
    assert r.status_code == 422
    assert r.json()["error"]["type"] == "validation_error"
    assert answers["A01"].ai_answer[:40] not in r.text  # sanitized: input not echoed


def test_classify_404_unknown_primary_brand(client_with, answers):
    c = client_with(single([]))
    r = c.post("/classify", json=body(answers["A01"], brand_id="acmesound"))
    assert r.status_code == 404 and r.json()["error"]["type"] == "unknown_primary_brand"


@pytest.mark.parametrize("steps,code,etype", [
    ([lookup(), text_response("not json")], 502, "malformed_output"),
    ([ProviderError("provider returned HTTP 500 (InternalServerError)")], 502, "provider_error"),
    ([lookup(), ProviderTimeout("provider request exceeded 5s timeout")], 504, "provider_timeout"),
    ([lookup(), lookup(), lookup()], 502, "turn_limit_exhausted"),
])
def test_classify_error_mapping(client_with, answers, steps, code, etype):
    c = client_with(single(steps))
    r = c.post("/classify", json=body(answers["A01"]))
    assert r.status_code == code
    assert r.json() == {"error": {"type": etype, "message": r.json()["error"]["message"]}}
    assert "sk-ant" not in r.text and "Traceback" not in r.text


# ------------------------------------------------------------------ evaluation runs
def mixed_check_factory(gold, answers):
    """A41 empty-but-valid, A42 provider error, A43 invalid output, rest ok with one claim."""
    scripts = {}
    for i in range(41, 51):
        aid = f"A{i}"
        a = answers[aid]
        first_sentence = a.ai_answer.split(". ")[0] + "."
        scripts[aid] = [lookup(a.brand_id), text_response({"answer_id": aid, "claims": [
            {"quote": first_sentence, "label": "unknown", "fact_ids": [], "reason": "Test."}]})]
    scripts["A41"] = [lookup(answers["A41"].brand_id), text_response({"answer_id": "A41", "claims": []})]
    scripts["A42"] = [ProviderError("provider returned HTTP 529 (OverloadedError)")]
    scripts["A43"] = [lookup(answers["A43"].brand_id), text_response("{oops")]
    s = ScriptedByAnswer(scripts)
    return ProviderFactory(s.for_answer, "fake", "fake-model")


def test_check_run_persists_all_outcomes_with_null_quality(client_with, answers, gold, db):
    c = client_with(mixed_check_factory(gold, answers))
    r = c.post("/evaluation-runs", json={"agent_version": "v1", "split": "check"})
    assert r.status_code == 201
    data = r.json()
    assert data["status"] == "completed" and data["metrics"] is None
    cnt = data["counts"]
    assert cnt["scheduled_answers"] == 10 and cnt["ok_answers"] == 8 and cnt["error_answers"] == 2
    assert cnt["empty_ok_answers"] == 1 and cnt["P"] == 7
    assert cnt["G"] is None and cnt["M"] is None and cnt["C"] is None

    g = c.get(f"/evaluation-runs/{data['run_id']}")
    assert g.status_code == 200
    run = g.json()
    assert [a["answer_id"] for a in run["answers"]] == [f"A{i}" for i in range(41, 51)]
    by = {a["answer_id"]: a for a in run["answers"]}
    assert by["A41"]["status"] == "ok" and by["A41"]["claims"] == []
    assert by["A42"]["status"] == "error" and by["A42"]["error_type"] == "provider_error" and by["A42"]["claims"] == []
    assert by["A43"]["error_type"] == "malformed_output"
    assert all(cl["gold_match"] is None and cl["expected_label"] is None
               for a in run["answers"] for cl in a["claims"])
    assert run["scores"] is None and run["dataset_version"] == "long-brand-answers-50-v4"
    assert set(run["file_hashes"]) == {"answers.csv", "brand_facts.csv", "development_gold.csv"}
    assert run["settings"]["max_turns"] == 3 and run["settings"]["request_timeout_s"] == 5.0


def test_development_run_scores_and_marks_matches(client_with, answers, gold, db):
    scripts = {aid: perfect_script(gold, a) for aid, a in answers.items() if a.split == "development"}
    scripts["A02"] = [ProviderTimeout("provider request exceeded 5s timeout")]
    s = ScriptedByAnswer(scripts)
    c = client_with(ProviderFactory(s.for_answer, "fake", "fake-model"))
    r = c.post("/evaluation-runs", json={"agent_version": "v2", "split": "development"})
    assert r.status_code == 201
    d = r.json()
    n_a02 = sum(1 for g in gold if g.answer_id == "A02")
    assert d["counts"]["G"] == 376 and d["counts"]["P"] == 376 - n_a02 and d["counts"]["error_answers"] == 1
    assert d["metrics"]["joint_precision"] == 1.0
    assert d["metrics"]["joint_recall"] == pytest.approx((376 - n_a02) / 376)
    run = c.get(f"/evaluation-runs/{d['run_id']}").json()
    assert len(run["answers"]) == 40
    assert all(cl["gold_match"] is True and cl["label_correct"] is True
               for a in run["answers"] for cl in a["claims"])
    assert len(run["diagnostics"]["missed_gold_ids"]) == n_a02


def test_get_run_404_and_422(client_with):
    c = client_with(single([]))
    assert c.get(f"/evaluation-runs/{uuid.uuid4()}").status_code == 404
    r = c.get("/evaluation-runs/not-a-uuid")
    assert r.status_code == 422


def test_evaluation_run_request_validation(client_with):
    c = client_with(single([]))
    assert c.post("/evaluation-runs", json={"agent_version": "v1", "split": "final"}).status_code == 422
    assert c.post("/evaluation-runs", json={"agent_version": "v1", "split": "check",
                                            "gold": []}).status_code == 422


# ------------------------------------------------------------------ DB constraints / failure handling
def test_db_unique_constraints(db):
    meta = {"split": "check", "agent_version": "v1", "prompt_version": "p", "prompt_sha256": "x",
            "dataset_version": "d", "evaluator_version": "e", "fact_version": "f", "provider": "fake",
            "model": "m", "settings": {}, "file_hashes": {}}
    run_id = db.create_run(meta)
    res = {"answer_id": "A41", "status": "ok", "latency_ms": 1, "turns": 2}
    claim = {"claim_id": "A41:0:5", "start_char": 0, "end_char": 5, "quote": "abcde", "label": "unknown",
             "fact_ids": [], "reason": "r"}
    db.save_answer_result(run_id, 0, res, [claim])
    with pytest.raises(psycopg.errors.UniqueViolation):
        db.save_answer_result(run_id, 1, res, [])
    with pytest.raises(psycopg.errors.UniqueViolation):
        db.save_answer_result(run_id, 1, {**res, "answer_id": "A42"},
                              [{**claim, "claim_id": "A42:0:5"}, {**claim, "claim_id": "A42:0:5"}])
    # the failed transaction left no partial A42 row
    assert [a["answer_id"] for a in db.get_run(run_id)["answers"]] == ["A41"]
    with pytest.raises(psycopg.errors.CheckViolation):
        db.save_answer_result(run_id, 2, {"answer_id": "A43", "status": "error", "latency_ms": 1, "turns": 1}, [])


def test_infrastructure_failure_marks_run_failed_and_keeps_partial(db, answers, gold, settings, store):
    calls = {"n": 0}

    def factory(aid):
        calls["n"] += 1
        if calls["n"] == 3:
            raise RuntimeError("infrastructure down")
        return FakeProvider([lookup(answers[aid].brand_id), text_response({"answer_id": aid, "claims": []})])

    s = run_evaluation("v1", "check", ProviderFactory(factory, "fake", "m"), "fake", "m", db, settings, store)
    assert s["status"] == "failed"
    run = db.get_run(uuid.UUID(s["run_id"]))
    assert run["status"] == "failed" and run["failure_reason"] == "RuntimeError"
    assert [a["answer_id"] for a in run["answers"]] == ["A41", "A42"]
