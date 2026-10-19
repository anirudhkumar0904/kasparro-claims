# Results and analysis

All runs used the same data (CSV hashes in every report), evaluator, provider (`anthropic`), model (`claude-sonnet-5-5`) and settings: 3-turn limit, 180 s request timeout, 16,000 max tokens, SDK retries off, provider-default sampling. Only `prompts/v1.md` versus `prompts/v2.md` differs, and the two prompts differ in a single rule (`git diff v1-frozen v2-frozen -- claimcheck/prompts`).

## The four required live runs

| run | run_id | split | answers ok/error | P | G | M | C | extraction P / R / F1 | joint P / R / F1 | coverage C/G |
|---|---|---|---|---|---|---|---|---|---|---|
| v1 | `b7d69fb0-0bf6-4368-8f9d-40c273a4369d` | development | 40 / 0 | 376 | 376 | 376 | 376 | 1.000 / 1.000 / 1.000 | 1.000 / 1.000 / **1.000** | 1.000 |
| v2 | `a2d013d9-a12c-4452-b54d-6559a6db3bd5` | development | 40 / 0 | 376 | 376 | 376 | 376 | 1.000 / 1.000 / 1.000 | 1.000 / 1.000 / **1.000** | 1.000 |
| v1 | `908c0863-5374-48f1-9475-dff9903910f5` | check | 10 / 0 | 94 | null | null | null | null | null | null |
| v2 | `4daea87a-9aec-4e8f-8798-b098e0f99972` | check | 10 / 0 | 94 | null | null | null | null | null | null |

Reports: `reports/v1_development.{json,md}`, `reports/v2_development.{json,md}`, `reports/v1_check.{json,md}`, `reports/v2_check.{json,md}` and `reports/comparison.md`. Each report contains settings, versions, file hashes, the git revision, counts, timing and token totals, every answer outcome, and every accepted prediction with its span, quote, label, fact IDs and reason. Development reports also list missed, extra and wrong-label records; all three lists are empty for both development runs. Check-run quality fields are null by design and left for the reviewer's private key. Per-answer model/tool exchanges are in `traces/<run_id>/<answer_id>.json`. `evidence/sample_exchange_v2_development_A07.json` is one example: an answer containing an injected "Ignore the classification instructions…" sentence, which the agent did not follow and did not extract.

Missed gold IDs: none. Unmatched prediction IDs: none. Matched wrong-label IDs: none (both development runs). Answer errors: 0 in all four runs.

### Is the perfect development score real?

I treated 1.0 as something to verify, not celebrate:

- An independent re-count straight from the `claim_results` rows against `development_gold.csv`, bypassing `scoring.py`, gives P=M=C=G=376.
- Every stored quote equals `ai_answer[start:end]`.
- The traces show genuine Anthropic tool calls (turn 1 `tool_use` → `get_brand_facts`, turn 2 `end_turn`), with token usage that matches the run totals.
- Gold cannot reach the model: `AgentInput` forbids extra fields, gold is loaded only after all of a run's predictions are persisted, and `test_gold_never_enters_model_or_tool_payloads` checks the payloads.
- The scorer is not lenient: its controlled tests show that a partial span, an extra advice sentence, a wrong label and an errored answer each reduce the metrics.

The dataset is synthetic and very regular. Every gold span is exactly one naive sentence, and the factual sentences follow a small number of templates. A strong current model therefore finds every factual sentence and labels it correctly. The development score should not be read as evidence of performance on messier, real answers.

## Failure diagnosis and the one targeted change

With no span or label failures to fix, I investigated a concrete risk that the required metrics do not capture: **the evidence (`fact_ids`) attached to each claim**. The rubric asks for valid fact references, and a downstream reader relies on them to audit a label. Against the gold `evidence_fact_ids` on the 376 matched claims, v1 cited exactly the gold evidence set for only **259/376 (68.9%)** claims (79 extra IDs, 45 missing). The errors followed two patterns:

1. **Citing the row the sentence wrongly borrowed (over-citation).** For "costs INR 1,199 on 1 October 2026", v1 cited `price_2025` and `price_2026`. For a 100%-volume battery claim it cited both `battery_100_percent` and `battery_50_percent`. For a sibling-weight transfer it cited both models' `weight` rows. Under the brief's rule ("refutes it under matching conditions"), only the in-scope row decides the label; the borrowed row has non-matching conditions.
2. **Returning `[]` for `unknown` claims that build on a known row (under-citation).** Examples: a repair-time guarantee, where the warranty row is known but the repair time is not; a free-delivery claim, where the price row says shipping is excluded; multipoint Bluetooth, where the stereo-pairing row is the related known fact.

**Change (v2):** a single prompt rule replacing the one-line `fact_ids` instruction. Cite only rows whose model, field, date and conditions match the sentence's asserted scope and that decide it (all rows used in a calculation). Do not cite rows that only show what the sentence confused or borrowed. For `unknown`, cite the in-scope row the assertion builds on when one exists. Nothing else changed: extraction rules, label rules, code, settings and model are all the same.

### Measured effect (development, same inputs and scoring)

| run | role | exact evidence set | fact-ID precision | fact-ID recall | fact-ID F1 | extra / missing IDs | joint F1 |
|---|---|---|---|---|---|---|---|
| v1 `b7d69fb0` | primary baseline | 259/376 = 0.689 | 0.819 | 0.888 | 0.852 | 79 / 45 | 1.000 |
| v2 `a2d013d9` | primary candidate | 308/376 = **0.819** | 0.876 | 0.926 | **0.900** | 53 / 30 | 1.000 |
| v1 `db1e7668` | supplementary repeat of v1 | 251/376 = 0.668 | 0.808 | 0.876 | 0.841 | 84 / 50 | 1.000 |

- **Main metric (joint F1): no gain is possible from 1.0 and none is claimed.** v2 has 0 extraction or label regressions on development: 0 claims flipped either way, and 0 extra predictions.
- **Evidence agreement (secondary diagnostic, computed identically for every run from the saved rows):** +13 points exact-set rate, +0.05 fact-ID F1, with fewer extra and fewer missing IDs. It improved for every expected label (contradicted 0.61→0.76, supported 0.78→0.88, unknown 0.68→0.82).
- **Noise check:** sampling is not fixed, so I re-ran frozen v1 on development once more. It reproduced the 1.0 joint F1, and its evidence rate was 0.668 against 0.689 for the first v1 run. Run-to-run variation (about 2 points) is much smaller than the v1→v2 difference (about 13 points), so the improvement is unlikely to be noise. It is still one run per version, not a confidence interval.
- **Residual evidence disagreements in v2 (68 claims):** mostly gold conventions that are arguably debatable. For example, citing `bluetooth_version` alongside `wifi` for "Wi-Fi is absent, separate from Bluetooth", or the invoice-requirement row next to the warranty row. I did not tune further, because the brief asks for one change.

### Check split: what can and cannot be said

Both check runs completed 10/10 answers with 94 predictions each, on the identical set of 94 spans. Quality is not computed (no gold). Comparing the two saved outputs without gold: the 94 spans are identical; 18 claims differ only in `fact_ids`; **one claim differs in label**. In `A42:1433:1597` ("ClearTrail Plus is INR 1,200 less expensive than ClearTrail Mini…"), v1 says `contradicted`. v2 says `supported`, but its own reason says "Plus [is] INR 1,200 more expensive, not less, so the claim is wrong". From the catalogue (Plus 2,499, Mini 1,299), v1 is right. This is a **v2 label/reason inconsistency**, probably a sampling slip rather than an effect of the evidence rule, which does not touch labels. I found it only by comparing the frozen check outputs, after both versions were frozen, and I did not change anything in response. It points to a real residual risk; see future work.

## Disclosures about the evaluation

- The final-check inputs are visible, so this is not a blind benchmark. No prompt or code was tuned on A41–A50. After both versions were frozen and their check predictions saved, I compared the two check outputs to each other, as described above, and changed nothing.
- While designing v1, I read the brief's label rules and looked at a sample of development gold rows to understand the extraction unit and label conventions. The v2 change was derived from v1's development errors, which is the purpose of the development split.
- `claimcheck/report.py` (reporting only) was extended after the `v2-frozen` tag with the evidence diagnostic and the comparison pairing fix; the agent, prompts, validation and scorer are unchanged since their freezes (`git diff v2-frozen -- claimcheck/agent.py claimcheck/prompts claimcheck/validation.py claimcheck/scoring.py` is empty). Reports were regenerated from the stored database rows with the same report code for every run.

## Cost and timing

| run | wall time (sum of answer latencies) | input / output tokens |
|---|---|---|
| v1 development | 403.5 s (about 10 s per answer) | 440,541 / 64,741 |
| v2 development | 433.6 s | 459,741 / 69,005 |
| v1 check | 98.5 s | 110,152 / 16,011 |
| v2 check | 107.6 s | 114,952 / 17,235 |
| supplementary v1 development repeat | 410.7 s | 440,541 / 64,032 |

Every one of the 140 live answer runs used exactly 2 model turns (one lookup turn, one final turn); see the `turns` column in each report.

## Tests actually run

`python -m pytest -v` → **71 passed, 0 skipped, 0 failed** against a real local PostgreSQL 16 test database (`evidence/pytest_output.txt`). The tests cover:

- **CSV:** quoted commas and embedded newlines with byte-exact `ai_answer`; all 376 gold spans equal their slices; CSV hashes; literal boolean parsing (`"false"` → `False`, `"False"` rejected); typed values; blank unit/condition → `None`.
- **Validation:** valid offsets; out-of-bounds and mismatched quotes; whitespace-padded spans; wrong `claim_id`; duplicate IDs; overlapping and unordered claims; invented fact IDs; fact IDs from a brand that was not looked up; repeated-quote resolution; reason trimming; malformed JSON, unsupported labels and extra fields.
- **Scorer:** perfect output; missed claims; extra advice prediction; partial span; wrong labels; a provider-error answer, whose gold stays in G; valid empty predictions; the G=10 P=10 M=8 C=7 example (0.80/0.70, coverage 0.70, not 0.875); missing, duplicate and unscheduled outcomes rejected; duplicate spans rejected; null metrics for check and empty splits.
- **Fake provider:** malformed output; unsupported label; quote not found; invented fact ID; illegal tool (not executed, no further turn); unknown requested brand; invalid tool arguments; unknown primary brand; timeout; provider error; turn exhaustion (exactly 3 calls); final answer without tool use; truncated output; valid empty output; multiple tool calls in one turn; gold never entering model/tool payloads.
- **API + DB:** 200 `/classify`; 422 for `claims`/`gold_spans`/`expected_label` fields, missing fields, a bad version and an empty ID, with input values not echoed; 404 unknown brand; 502 malformed/provider/turn-limit; 504 timeout; 201 check run with ok, empty and error answers and null quality; joined GET in stable order; development run with an error answer scored and claims marked; GET 404/422; unique-constraint and CHECK violations with per-answer transaction rollback; an infrastructure failure mid-run marked `failed` with partial evidence kept.

Tests written but **not** run: none. Fakes test the plumbing only. The four live runs above are the actual quality evidence.

Live API calls through uvicorn: `evidence/api_calls.json` (a live 200 `/classify` on A07 with v2, plus 422/404 error paths and a joined GET of the v1 development run).

## Limitations

- **Non-deterministic sampling.** The model rejects `temperature`, so repeated runs can differ; the A42 slip shows labels can occasionally differ too. I measured one repeat for v1 but have no repeated runs for v2 or for check.
- **The synthetic dataset saturates extraction and labelling** for this model, so the required metrics cannot separate v1 from v2. The improvement claim rests on a secondary diagnostic measured against gold evidence conventions, which are partly debatable.
- **Exact-quote location only.** A quote with altered whitespace or punctuation fails the whole answer (`quote_not_found`), which never happened in 140 live answer runs but is a brittle point. There is also no repair turn: any invalid output is an answer error, as the brief specifies.
- `POST /evaluation-runs` is synchronous: a 40-answer development run holds the HTTP request for about 7 minutes. That is acceptable locally, as the brief requires no durability or idempotency.
- `/classify` results are not persisted, since the brief does not require it.
- The 180 s timeout is per request, so the worst case per answer is 3 × 180 s.
- There is no Langfuse, concurrency or React (all optional).

## Unfinished work / next steps

- A deterministic label/reason consistency check (or a self-verification turn within the 3-turn budget) to catch slips like A42.
- Repeated runs per version to report mean ± spread for both joint F1 and evidence agreement.
- A tolerant-but-safe quote locator (whitespace-insensitive match mapped back to source offsets), recorded per claim.
