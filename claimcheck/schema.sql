-- Evaluation run storage. Applied idempotently at startup (CREATE ... IF NOT EXISTS).

CREATE TABLE IF NOT EXISTS runs (
    run_id            UUID PRIMARY KEY,
    created_at        TIMESTAMPTZ NOT NULL DEFAULT now(),
    finished_at       TIMESTAMPTZ,
    status            TEXT NOT NULL CHECK (status IN ('running', 'completed', 'failed')),
    split             TEXT NOT NULL CHECK (split IN ('development', 'check')),
    agent_version     TEXT NOT NULL CHECK (agent_version IN ('v1', 'v2')),
    prompt_version    TEXT NOT NULL,
    prompt_sha256     TEXT NOT NULL,
    dataset_version   TEXT NOT NULL,
    evaluator_version TEXT NOT NULL,
    fact_version      TEXT NOT NULL,
    provider          TEXT NOT NULL,
    model             TEXT NOT NULL,
    settings          JSONB NOT NULL,
    source_revision   TEXT,
    file_hashes       JSONB NOT NULL,
    counts            JSONB,
    scores            JSONB,          -- metrics; NULL for check runs
    diagnostics       JSONB,          -- missed / unmatched / wrong-label id lists (development only)
    failure_reason    TEXT
);

CREATE TABLE IF NOT EXISTS answer_results (
    id            BIGSERIAL PRIMARY KEY,
    run_id        UUID NOT NULL REFERENCES runs(run_id) ON DELETE CASCADE,
    answer_id     TEXT NOT NULL,
    ordinal       INTEGER NOT NULL,
    status        TEXT NOT NULL CHECK (status IN ('ok', 'error')),
    error_type    TEXT,
    error_message TEXT,
    latency_ms    INTEGER NOT NULL,
    turns         INTEGER NOT NULL,
    input_tokens  INTEGER,
    output_tokens INTEGER,
    n_claims      INTEGER NOT NULL DEFAULT 0,
    trace_ref     TEXT,
    created_at    TIMESTAMPTZ NOT NULL DEFAULT now(),
    CONSTRAINT answer_results_run_answer_uq UNIQUE (run_id, answer_id),
    CONSTRAINT answer_error_consistency CHECK (
        (status = 'ok' AND error_type IS NULL) OR (status = 'error' AND error_type IS NOT NULL AND n_claims = 0))
);

CREATE TABLE IF NOT EXISTS claim_results (
    id             BIGSERIAL PRIMARY KEY,
    run_id         UUID NOT NULL,
    answer_id      TEXT NOT NULL,
    claim_id       TEXT NOT NULL,
    start_char     INTEGER NOT NULL CHECK (start_char >= 0),
    end_char       INTEGER NOT NULL,
    quote          TEXT NOT NULL,
    label          TEXT NOT NULL CHECK (label IN ('supported', 'contradicted', 'unknown')),
    fact_ids       JSONB NOT NULL,
    reason         TEXT NOT NULL,
    -- optional development match, filled only after predictions are saved
    gold_match     BOOLEAN,
    gold_claim_id  TEXT,
    expected_label TEXT,
    label_correct  BOOLEAN,
    CONSTRAINT claim_span_valid CHECK (end_char > start_char),
    CONSTRAINT claim_results_span_uq UNIQUE (run_id, answer_id, start_char, end_char),
    CONSTRAINT claim_results_answer_fk FOREIGN KEY (run_id, answer_id)
        REFERENCES answer_results(run_id, answer_id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS answer_results_run_idx ON answer_results (run_id, ordinal);
CREATE INDEX IF NOT EXISTS claim_results_run_idx ON claim_results (run_id, answer_id, start_char);

-- An error answer may never carry claim rows (enforced in the database, not only via n_claims).
CREATE OR REPLACE FUNCTION claim_requires_ok_answer() RETURNS trigger AS $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM answer_results
                    WHERE run_id = NEW.run_id AND answer_id = NEW.answer_id AND status = 'ok') THEN
        RAISE EXCEPTION 'claim rows require an ok answer result' USING ERRCODE = '23514';
    END IF;
    RETURN NEW;
END $$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS claim_requires_ok_answer ON claim_results;
CREATE TRIGGER claim_requires_ok_answer BEFORE INSERT OR UPDATE OF run_id, answer_id ON claim_results
    FOR EACH ROW EXECUTE FUNCTION claim_requires_ok_answer();
