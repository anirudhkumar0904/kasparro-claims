# Four-run comparison

| run | split | status | ok/err | P | G | M | C | ext P | ext R | ext F1 | joint P | joint R | joint F1 | coverage C/G |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| v1 `b7d69fb0` | development | completed | 40/0 | 376 | 376 | 376 | 376 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | **1.0000** | 1.0000 |
| v2 `a2d013d9` | development | completed | 40/0 | 376 | 376 | 376 | 376 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | **1.0000** | 1.0000 |
| v1 `908c0863` | check | completed | 10/0 | 94 | null | null | null | null | null | null | null | null | **null** | null |
| v2 `4daea87a` | check | completed | 10/0 | 94 | null | null | null | null | null | null | null | null | **null** | null |
| v1 `db1e7668` | development | completed | 40/0 | 376 | 376 | 376 | 376 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | **1.0000** | 1.0000 |

## Evidence agreement on development (secondary diagnostic)

| run | matched claims | exact-set rate | fact-ID precision | fact-ID recall | fact-ID F1 | fp | fn |
|---|---|---|---|---|---|---|---|
| v1 `b7d69fb0` (primary) | 376 | 0.6888 | 0.8192 | 0.8883 | 0.8524 | 79 | 45 |
| v2 `a2d013d9` (primary) | 376 | 0.8191 | 0.8756 | 0.9256 | 0.8999 | 53 | 30 |
| v1 `db1e7668` (supplementary repeat) | 376 | 0.6676 | 0.8078 | 0.8759 | 0.8405 | 84 | 50 |

## Development v1 → v2 per-claim changes

- gold claims fixed by v2 (not correct in v1, correct in v2): **0**
- regressions (correct in v1, not correct in v2): **0**
- extra predictions: v1 0, v2 0 (new in v2: 0, removed: 0)

### Fixed


### Regressed



## Check split: v1 vs v2 saved outputs (no gold; not a quality score)

- spans: v1 94, v2 94, shared 94, only v1 0, only v2 0
- shared spans with a different label: 1
- shared spans with different fact_ids only: 18

- `A42:1433:1597` v1 **contradicted** / v2 **supported**: For a current India catalogue comparison before shipping, ClearTrail Plus is INR 1,200 less expensive than ClearTrail Mini, with tax included in both listed prices.
  - v1 reason: Plus is INR 2,499 and Mini is INR 1,299, so Plus costs INR 1,200 more, not less.
  - v2 reason: The 2026 prices are INR 2,499 for Plus and INR 1,299 for Mini, both tax included. That makes Plus INR 1,200 more expensive, not less, so the claim is wrong.
