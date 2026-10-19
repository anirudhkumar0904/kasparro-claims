# claimcheck: extract and classify claims in long AI answers

A Python agent that reads a long AI-written answer about speaker products, finds every factual claim sentence, and labels each one `supported`, `contradicted` or `unknown`. The only evidence is the supplied catalogue, which the model fetches with live `get_brand_facts` tool calls. It also includes a deterministic exact-span harness, a preserved v1 baseline and v2 candidate, a thin FastAPI service backed by PostgreSQL, and controlled tests.

- Dataset `long-brand-answers-50-v4`, facts `speaker-catalogue-v4`, evaluator `sentence-spans-and-labels-v4`
- Provider/model for all four runs: Anthropic `claude-sonnet-5-5`
- Results and analysis: **[RESULTS.md](RESULTS.md)**. Saved run reports: [`reports/`](reports/). Raw console logs and test output: [`evidence/`](evidence/)

## Layout

```
claimcheck/
  config.py            settings + fixed version identifiers (timeout, turn limit, model, ...)
  data.py              csv-module loading, exact text preservation, typed fact values, file hashes
  facts_tool.py        read-only get_brand_facts(brand_id) + JSON-schema tool spec
  providers/           Anthropic Messages API provider, scripted FakeProvider for tests
  agent.py             3-turn tool-calling loop, tool executor allow-list, error handling, trace
  validation.py        quote -> offset location in Python, full output validation
  scoring.py           exact span matching, extraction + joint P/R/F1, missed/extra/wrong-label
  runner.py            sequential evaluation run: predict + persist, then (dev only) join gold and score
  db.py, schema.sql    PostgreSQL (psycopg 3, parameterized SQL, FKs + unique constraints)
  api.py               FastAPI: POST /classify, POST /evaluation-runs, GET /evaluation-runs/{id}
  report.py, cli.py    JSON/Markdown run reports, four-run comparison, CLI
  prompts/v1.md        frozen baseline prompt (git tag v1-frozen)
  prompts/v2.md        frozen candidate prompt (git tag v2-frozen); only the fact_ids rule differs
data/                  the issued CSVs, unmodified, plus SHA256SUMS
reports/               the four saved live-run reports (.json + .md) and comparison.md
traces/<run_id>/       sanitized per-answer model/tool exchanges for every live run
evidence/              console logs of the live runs, pytest output, API call samples
tests/                 controlled tests (fake provider, real local PostgreSQL)
scripts/recount_from_db.py   independent recount of stored development scores (bypasses scorer)
```

## Setup

Requirements: Python 3.13 (tested with 3.13.16) and PostgreSQL 16 (tested with 16.15). Exact dependency versions are pinned in `requirements.txt`.

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# PostgreSQL: create a role and two databases (app + tests)
sudo -u postgres psql -c "CREATE ROLE claimcheck LOGIN PASSWORD 'claimcheck';"
sudo -u postgres createdb -O claimcheck claimcheck
sudo -u postgres createdb -O claimcheck claimcheck_test

cp .env.example .env          # then set ANTHROPIC_API_KEY; DATABASE_URL defaults to the DB above
python -m claimcheck.cli init-db
```

`DATABASE_URL` format: `postgresql://USER:PASSWORD@HOST:5432/DBNAME`. The `.env` file is git-ignored; never commit it. Optional overrides (model, timeout, turn limit, token budget) are documented in `.env.example`. Keep them identical across v1 and v2.

Check that the data is the issued data: `cd data && sha256sum -c SHA256SUMS`.

## Run

```bash
# The required sequence (each command saves to PostgreSQL and writes reports/<name>.json|.md)
python -m claimcheck.cli run --agent-version v1 --split development --report-name v1_development
python -m claimcheck.cli run --agent-version v2 --split development --report-name v2_development
python -m claimcheck.cli run --agent-version v1 --split check       --report-name v1_check
python -m claimcheck.cli run --agent-version v2 --split check       --report-name v2_check
python -m claimcheck.cli compare <v1_dev_id> <v2_dev_id> <v1_check_id> <v2_check_id>   # -> reports/comparison.md
python -m claimcheck.cli report <run_id> --name <name>   # re-export any stored run

# API
uvicorn claimcheck.api:app --port 8000
curl -s -X POST localhost:8000/classify -H 'content-type: application/json' \
  -d '{"answer_id":"A01","brand_id":"cleartrail","question":"...","ai_answer":"...","agent_version":"v2"}'
curl -s -X POST localhost:8000/evaluation-runs -H 'content-type: application/json' \
  -d '{"agent_version":"v1","split":"check"}'          # synchronous; returns 201 when finished
curl -s localhost:8000/evaluation-runs/<run_id>
```

## Test

```bash
python scripts/recount_from_db.py <dev_run_id>   # independent recount of stored scores from DB rows
python -m pytest -v          # uses TEST_DATABASE_URL (default: local claimcheck_test); DB tests skip if unreachable
```

The actual output of the run used for submission is in [`evidence/pytest_output.txt`](evidence/pytest_output.txt). See "Tests actually run" in RESULTS.md.

## Design

**Agent input and isolation.** The model sees exactly `answer_id`, `brand_id`, `question` and `ai_answer` inside an `<answer_record>` block that is marked as untrusted data. `AgentInput` forbids extra fields, so gold spans, labels or claim lists cannot be passed in (the API returns 422). Gold is loaded only by the scorer, after every prediction of a run has been persisted. A test asserts that no gold claim ID, explanation or gold field name appears in any model or tool payload.

**Tool use.** `get_brand_facts(brand_id)` is offered through native Anthropic tool calling, with a JSON schema that enumerates the known brands. The executor accepts only that tool name with exactly one string `brand_id` argument. Any other tool name, malformed arguments or an unknown brand is an answer-level error, and nothing is executed. Several lookups in one turn are allowed, which is how the model fetches a comparison brand. The tool returns the brand's typed rows with `fact_version: speaker-catalogue-v4`. A final answer produced without any lookup is rejected (`no_tool_use`).

**Limits.** At most 3 model turns per answer. Every provider request has a **180 s timeout** (`CLAIMCHECK_TIMEOUT_S`). SDK automatic retries are disabled (`max_retries=0`) so every model call appears in the trace. The token budget is 16,000. The model rejects a `temperature` parameter, so sampling is the provider default; runs are therefore not bit-reproducible (see limitations).

**Offsets.** The model returns verbatim sentence quotes, never offsets. Python locates each quote in the exact decoded `ai_answer` (zero-based code points, end exclusive). Repeated identical text is resolved in document order: each quote takes the first free occurrence at or after the previous claim's end. Python then derives `claim_id = answer_id:start:end`, sorts the claims, and validates bounds, quote equality, no surrounding whitespace, unique IDs, no overlaps, labels, existing fact IDs, and that each fact ID belongs to a brand actually looked up in this answer. `reason` is trimmed to at most two sentences rather than failing the answer.

**Errors.** Provider failure, timeout, malformed or invalid output, illegal tool, unknown requested brand, truncated output and turn exhaustion all produce `status=error` with a sanitized `error_type`/`error_message` and **zero** accepted predictions. An error is never converted to `unknown`. The API maps these to 502 (504 for timeout, 404 for an unknown primary brand, 422 for invalid requests). A missing API key gives 502 `provider_not_configured`; a missing `DATABASE_URL` gives 503.

**Persistence.** `runs` → `answer_results` → `claim_results`, linked by `run_id` with foreign keys. Constraints: unique `(run_id, answer_id)`, unique `(run_id, answer_id, start_char, end_char)`, label and status CHECKs, and a trigger that rejects claim rows for an error answer. Each answer's terminal row and its claims are written in one transaction as soon as that answer finishes, so an interrupted run keeps its partial evidence and is marked `failed`. Run rows hold split, agent/prompt (path + SHA-256)/dataset/evaluator/fact versions, provider, model, settings, git revision, CSV hashes, counts, scores (NULL for check runs) and development diagnostics as JSONB.

**Scoring.** Matching is exact on `(answer_id, start_char, end_char)` after quote equality is validated; each gold span matches at most one prediction. Extraction P = M/P, R = M/G, F1 = 2M/(P+G); joint P = C/P, R = C/G, F1 = 2C/(P+G). Zero denominators give 0 when gold exists; an empty split gives null. Reports also list coverage C/G, missed gold IDs, unmatched prediction IDs, matched wrong-label IDs and answer error counts. Missing or duplicated answer outcomes are rejected. For check runs, G/M/C, matches, expected labels and all quality metrics are null.

## AI assistance disclosure

This project was built with substantial help from **Claude Code** (Anthropic), as the brief permits. Claude Code wrote most of the code, the prompts, the tests and this documentation, ran the four live runs on my API key, and drafted the analysis in RESULTS.md. The automated checks performed during the build were:

- an independent re-count of the development scores from raw database rows, bypassing the scorer;
- quote/offset equality for every stored claim;
- a secret scan of the repository, traces and reports;
- confirmation that the agent, prompt, validation and scorer code is unchanged since the freeze tags;
- the full test suite against a real PostgreSQL database;
- an independent review by a separate agent that had not seen the build. It recomputed every reported number, checked the hashes, freezes and secrets, and ran the tests from a fresh clone. Its findings were fixed or disclosed in RESULTS.md.

**What I verified myself:** _(fill in before submitting. For example: I read every module and can explain the agent loop, validation and scoring; I re-ran `pytest`; I re-derived the G=10 P=10 M=8 C=7 arithmetic; I checked a sample of predictions in `reports/*.md` against `brand_facts.csv`; I reviewed the A42 inconsistency.)_

**Time spent:** about 45 minutes of wall-clock time with Claude Code (13:13–13:58 IST, 19 October 2026), including about 26 minutes of live model runs. _(Add your own review time.)_

Git history: `v1-frozen` and `v2-frozen` tags mark the frozen agent versions; later commits only add run artifacts, reports and documentation.
