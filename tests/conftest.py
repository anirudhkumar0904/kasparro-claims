import os

import psycopg
import pytest

from claimcheck import config
from claimcheck.config import Settings
from claimcheck.data import load_answers, load_gold
from claimcheck.facts_tool import FactStore

TEST_DB_URL = os.getenv("TEST_DATABASE_URL", "postgresql://claimcheck:claimcheck@localhost:5432/claimcheck_test")


@pytest.fixture(scope="session")
def store():
    return FactStore()


@pytest.fixture(scope="session")
def answers():
    return {a.answer_id: a for a in load_answers()}


@pytest.fixture(scope="session")
def gold():
    return load_gold()


@pytest.fixture
def settings():
    return Settings(request_timeout_s=5.0, max_turns=3, max_tokens=1000)


@pytest.fixture(autouse=True)
def _isolate_traces(tmp_path, monkeypatch):
    monkeypatch.setattr(config, "TRACES_DIR", tmp_path / "traces")
    monkeypatch.setattr(config, "REPO_ROOT", tmp_path)


@pytest.fixture
def db():
    from claimcheck.db import Database

    try:
        psycopg.connect(TEST_DB_URL, connect_timeout=3).close()
    except Exception:
        pytest.skip("TEST_DATABASE_URL is not reachable; database tests skipped")
    database = Database(TEST_DB_URL)
    database.init_schema()
    with database.connect() as conn:
        conn.execute("TRUNCATE runs CASCADE")
    return database
