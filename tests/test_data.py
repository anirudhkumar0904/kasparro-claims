import csv

import pytest

from claimcheck import config
from claimcheck.data import (DataError, answers_for_split, load_answers, load_facts, load_gold,
                             parse_bool, parse_typed_value, sha256_file)


def test_quoted_commas_and_embedded_newlines_are_preserved(tmp_path):
    text = 'First, a sentence with "quotes", commas.\n\nSecond paragraph,  double  spaces. \n'
    p = tmp_path / "answers.csv"
    with open(p, "w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["answer_id", "split", "brand_id", "question", "ai_answer"])
        w.writerow(["X1", "development", "cleartrail", "Q, with comma?", text])
    raw = p.read_text(encoding="utf-8")
    assert raw.count("\n") > 2  # record spans several physical lines
    [a] = load_answers(p)
    assert a.ai_answer == text  # byte-exact: no strip, no whitespace normalisation
    assert a.question == "Q, with comma?"


def test_real_answers_shape_and_exact_offsets(answers):
    assert len(answers) == 50
    assert len(answers_for_split("development")) == 40
    assert [a.answer_id for a in answers_for_split("check")] == [f"A{i}" for i in range(41, 51)]
    assert any("\n" in a.ai_answer for a in answers.values())  # embedded newlines survive
    gold = load_gold(answers=list(answers.values()))  # raises if any gold span != ai_answer slice
    assert len(gold) == 376


def test_csv_hashes_match_issued_files():
    sums = dict(reversed(line.split()) for line in (config.DATA_DIR / "SHA256SUMS").read_text().splitlines())
    for name, digest in sums.items():
        assert sha256_file(config.DATA_DIR / name) == digest


def test_boolean_parsing_is_literal():
    assert parse_bool("true") is True
    assert parse_bool("false") is False  # never bool("false")
    for bad in ("False", "TRUE", "0", "", "yes"):
        with pytest.raises(DataError):
            parse_bool(bad)


def test_typed_fact_values():
    facts = {f.fact_id: f for f in load_facts()}
    assert len(facts) == 132
    assert facts["cleartrail.mini.wifi"].value is False
    assert facts["cleartrail.mini.cable_included"].value is True
    assert facts["cleartrail.mini.price_2026"].value == 1299 and isinstance(facts["cleartrail.mini.price_2026"].value, int)
    assert facts["cleartrail.mini.bluetooth_version"].value == "5.3"  # string stays string
    assert facts["cleartrail.mini.charging_port"].unit is None  # blank unit = not applicable
    assert facts["cleartrail.mini.model_name"].condition is None
    assert facts["cleartrail.mini.price_2025"].valid_to.isoformat() == "2025-12-31"
    assert parse_typed_value("2.5", "number") == 2.5
    with pytest.raises(DataError):
        parse_typed_value("x", "number")
