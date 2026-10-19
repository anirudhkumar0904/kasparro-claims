import pytest

from claimcheck.data import GoldClaim
from claimcheck.scoring import AnswerOutcome, PredClaim, ScoringInputError, score_split


def g(aid, s, e, label="supported"):
    return GoldClaim(aid, f"{aid}:{s}:{e}", s, e, "q", label, (), "", ())


def p(aid, s, e, label="supported"):
    return PredClaim(aid, f"{aid}:{s}:{e}", s, e, "q", label)


GOLD = [g("A", 0, 10), g("A", 11, 20, "unknown"), g("B", 0, 10, "contradicted")]
OK = [AnswerOutcome("A", "ok"), AnswerOutcome("B", "ok")]


def score(preds, outcomes=OK, gold=GOLD, ids=("A", "B")):
    return score_split("development", list(ids), outcomes, preds, gold)


def test_perfect_output():
    r = score([p("A", 0, 10), p("A", 11, 20, "unknown"), p("B", 0, 10, "contradicted")])
    assert r["metrics"] == {k: 1.0 for k in r["metrics"]}
    assert r["missed_gold_ids"] == [] and r["unmatched_prediction_ids"] == []


def test_missed_claim_reduces_recall():
    r = score([p("A", 0, 10), p("B", 0, 10, "contradicted")])
    assert r["counts"]["M"] == 2 and r["metrics"]["extraction_recall"] == pytest.approx(2 / 3)
    assert r["metrics"]["extraction_precision"] == 1.0
    assert r["missed_gold_ids"] == ["A:11:20"]


def test_extra_advice_prediction_reduces_precision():
    preds = [p("A", 0, 10), p("A", 11, 20, "unknown"), p("B", 0, 10, "contradicted"), p("B", 11, 30, "unknown")]
    r = score(preds)
    assert r["metrics"]["extraction_precision"] == 0.75
    assert r["metrics"]["joint_f1"] == pytest.approx(2 * 3 / 7)
    assert r["unmatched_prediction_ids"] == ["B:11:30"]


def test_partial_span_is_unmatched():
    r = score([p("A", 0, 9), p("A", 11, 20, "unknown"), p("B", 0, 10, "contradicted")])
    assert r["counts"]["M"] == 2 and "A:0:9" in r["unmatched_prediction_ids"]


def test_wrong_label_hits_joint_but_not_extraction():
    r = score([p("A", 0, 10), p("A", 11, 20, "supported"), p("B", 0, 10, "contradicted")])
    assert r["metrics"]["extraction_f1"] == 1.0
    assert r["metrics"]["joint_f1"] == pytest.approx(2 / 3)
    assert r["wrong_label_ids"] == [{"claim_id": "A:11:20", "predicted": "supported", "expected": "unknown"}]


def test_provider_error_answer_keeps_gold_as_missed():
    outcomes = [AnswerOutcome("A", "error", "provider_timeout"), AnswerOutcome("B", "ok")]
    r = score([p("B", 0, 10, "contradicted")], outcomes=outcomes)
    assert r["counts"]["G"] == 3 and r["counts"]["P"] == 1 and r["counts"]["error_answers"] == 1
    assert r["metrics"]["joint_recall"] == pytest.approx(1 / 3)
    assert r["metrics"]["joint_precision"] == 1.0
    assert set(r["missed_gold_ids"]) == {"A:0:10", "A:11:20"}
    assert r["answer_error_types"] == {"provider_timeout": 1}
    with pytest.raises(ScoringInputError):  # an errored answer may not carry predictions
        score([p("A", 0, 10)], outcomes=outcomes)


def test_valid_empty_predictions_score_zero():
    r = score([])
    assert r["counts"]["P"] == 0 and r["counts"]["empty_ok_answers"] == 2
    assert all(v == 0.0 for v in r["metrics"].values())


def test_arithmetic_example_g10_p10_m8_c7():
    gold = [g("A", i * 10, i * 10 + 5) for i in range(10)]
    preds = [p("A", i * 10, i * 10 + 5, "supported" if i < 7 else "unknown") for i in range(8)]
    preds += [p("A", 200, 205), p("A", 210, 215)]
    r = score_split("development", ["A"], [AnswerOutcome("A", "ok")], preds, gold)
    c, m = r["counts"], r["metrics"]
    assert (c["G"], c["P"], c["M"], c["C"]) == (10, 10, 8, 7)
    for k in ("extraction_precision", "extraction_recall", "extraction_f1"):
        assert m[k] == pytest.approx(0.80)
    for k in ("joint_precision", "joint_recall", "joint_f1"):
        assert m[k] == pytest.approx(0.70)
    assert r["gold_claim_coverage"] == pytest.approx(0.70)  # not the matched-only 7/8 = 0.875


def test_missing_or_duplicate_outcomes_rejected():
    with pytest.raises(ScoringInputError, match="missing"):
        score([], outcomes=[AnswerOutcome("A", "ok")])
    with pytest.raises(ScoringInputError, match="duplicate"):
        score([], outcomes=OK + [AnswerOutcome("A", "ok")])
    with pytest.raises(ScoringInputError, match="unscheduled"):
        score([], outcomes=OK + [AnswerOutcome("C", "ok")])


def test_duplicate_predicted_span_rejected():
    with pytest.raises(ScoringInputError):
        score([p("A", 0, 10), p("A", 0, 10)])


def test_check_split_quality_is_null():
    r = score_split("check", ["A"], [AnswerOutcome("A", "ok")], [p("A", 0, 10)], None)
    assert r["metrics"] is None and r["counts"]["G"] is None and r["counts"]["M"] is None
    assert r["counts"]["C"] is None and r["missed_gold_ids"] is None and r["per_claim"] is None
    assert r["counts"]["P"] == 1


def test_empty_scheduled_split_has_null_metrics():
    r = score_split("development", [], [], [], GOLD)
    assert r["metrics"] is None
