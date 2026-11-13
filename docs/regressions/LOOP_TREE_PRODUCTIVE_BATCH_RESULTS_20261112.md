# Productive tree regressions: terminal anchors and annual payout

Completed and independently verified November 12, 2026 America/Denver. The [frozen batch](LOOP_TREE_PRODUCTIVE_BATCH_PROTOCOL_20261112.md) answers open benchmark and payout/supply questions using existing scoped data. It adds no price interval, synchronized quote, future forecast or causal verdict. All prior estimates remain unchanged.

## Findings

1. **Novo's level and state regressions still lose to terminal anchors with matching training memory.** The earlier anchor conclusion was not simply an expanding-versus-rolling mismatch.
2. **There is a specific historical exception:** Novo's five-year expanding OLS activity model beats its matching terminal anchor by **6.81% pragmatic / 5.11% strict MSE**. It also beats simpler regressions on matched origins. The win does not survive the rolling window or ridge, and nonoverlap phases contain only one or two outcomes. Retain it as a scoped candidate, not general liquidity causality or prospective skill.
3. **Samsung's annual payout/supply association is weak in the available panel.** Fourteen annual changes yield about **2%** joint explanatory R², wide intervals and no established payout association. This limits the fitted annual design, not every payout-credibility or investor-demand mechanism.
4. **Differential class cash has no identifying variation here:** preferred-minus-common annual DPS is KRW1 on a post-split-equivalent basis in all fifteen fiscal years. A regression on that constant cannot test its effect.

## A. The missing terminal-anchor comparisons

We refit the existing LH-LEVEL, LH-STATE and LH-ACTIVITY OLS/fixed-lambda1-ridge regressions on every successful LH3 origin, both cleaning rules, two-/five-year horizons, expanding and the already fixed rolling120 training window. Every training label ends at or before its forecast origin. No new window, link, feature, penalty or security was selected.

The run reproduced **54,748 conditional forecast-method cases** across **131 source groups and eleven comparisons**, with **524 aggregate score rows**. Those are repeated method/feature/window/coverage cases, not independent market outcomes. The maximum difference from saved predictions was **2.85×10⁻¹⁴ pp**. All eight inherited failed rolling origins remain recorded; an entirely unavailable strict five-year activity group is not assigned a zero score. The previously diagnosed 316 impossible OLS terminal-discount cases remain visible rather than clipped.

The added benchmark forecasts `mean(matured terminal discounts) − today's discount`, using **the same training rows as each conditional model**. It is compared alongside persistence and mean historical change. Original ridge is fit to discount changes; refitting ridge to terminal levels would change its penalty center and was not silently done.

### Novo level-model result

R² below is relative to the **matching terminal anchor**, not persistence. Negative means the regression has higher historical MSE.

| Coverage | Horizon | Expanding OLS | Expanding ridge | Rolling OLS | Rolling ridge |
| --- | --- | ---: | ---: | ---: | ---: |
| Pragmatic | 24 months | −0.01138 | −0.17382 | −0.01569 | −0.20446 |
| Strict | 24 months | −0.01544 | −0.16394 | −0.02227 | −0.20263 |
| Pragmatic | 60 months | −0.03033 | −0.01438 | −0.06473 | −0.07706 |
| Strict | 60 months | −0.01948 | −0.01329 | −0.04807 | −0.06736 |

All sixteen level-model comparisons lose. All sixteen corresponding Novo state-model comparisons also lose. The original rolling OLS wins versus persistence and mean historical **change** remain intact: adding the relevant terminal **level** benchmark changes the claim we can make, not the old losses or predictions.

### Novo activity exception: preserve the win and its limits

| Fixed method | Coverage | Five-year origins | MSE reduction vs own matching anchor | Reduction vs level OLS on matched origins | Reduction vs state OLS on matched origins |
| --- | --- | ---: | ---: | ---: | ---: |
| Expanding activity OLS | Pragmatic | 88 | 6.81% | 5.46% | 7.60% |
| Expanding activity OLS | Strict | 74 | 5.11% | 4.12% | 4.55% |

State and activity models use identical training counts on these matched origins. Their measured increment is therefore not explained by a larger state-model training sample. The level model can use different training rows, so its same-origin comparison does not isolate one feature alone.

The exception has positive anchor-relative aggregate scores in every already fixed calendar bucket: pragmatic **35.28%/7.37%/4.12%** through 2014, 2015–2019 and 2020 onward; strict **47.80%/6.58%/3.40%**. Bucket sizes are only **7/60/21** and **3/52/19** origins, with overlapping five-year targets. These are not independent time replications. Only **31/60 pragmatic** and **28/54 strict** available nonoverlap phases beat the anchor, with just one or two outcomes in a phase.

Rolling activity OLS loses to its anchor; expanding ridge loses as well. Only **2 of Novo's 48** declared method/feature/window/horizon/coverage cases beat their anchors. These are overlapping specification cases, not a multiple-testing-adjusted discovery count. The activity variable remains a volume proxy, not an observed spread, depth, signed investor flow or borrow constraint. No new model is selected for deployment or automatically added to an issued prospective cohort.

### Entire comparison universe

Counts below show terminal-anchor wins, pragmatic / strict. Denominators are available class-specific samples; a benchmark win alone does not imply a persistence win.

| Model | Window | Method | 24 months | 60 months |
| --- | --- | --- | --- | --- |
| Level | Expanding | OLS | 2/11 / 2/11 | 4/11 / 4/11 |
| Level | Expanding | Ridge | 6/11 / 6/11 | 3/11 / 3/11 |
| Level | Rolling120 | OLS | 1/11 / 1/11 | 3/11 / 3/11 |
| Level | Rolling120 | Ridge | 5/11 / 5/11 | 3/11 / 3/11 |
| State | Expanding | OLS | 1/11 / 1/11 | 2/11 / 1/11 |
| State | Expanding | Ridge | 5/11 / 5/11 | 6/11 / 5/11 |
| State | Rolling120 | OLS | 0/11 / 0/11 | 2/11 / 1/11 |
| State | Rolling120 | Ridge | 4/11 / 4/11 | 3/11 / 2/11 |
| Activity | Expanding | OLS | 1/11 / 0/11 | 4/11 / 3/10 |
| Activity | Expanding | Ridge | 6/11 / 6/11 | 4/11 / 4/10 |
| Activity | Rolling120 | OLS | 0/11 / 0/11 | 2/11 / 1/10 |
| Activity | Rolling120 | Ridge | 4/11 / 5/11 | 2/11 / 2/10 |

The [complete 524-row scorecard](LOOP_TREE_PRODUCTIVE_BATCH_SCORES_20261112.csv) preserves every result against all three benchmarks. Sixty-five score cases beat both persistence and their matching anchor; they are highly dependent and cannot be counted as sixty-five discoveries. No universal predictor follows.

## B. Samsung delivered cash, supply and annual discount changes

We assembled **fifteen fiscal levels, FY2010–FY2024**, from thirteen identified pages of existing issuer reports. FY2010 comes from the earliest suitable FY2011 comparative; FY2013 from FY2014. Native values, share bases, source hashes, report vintages and unknown first-publication dates remain explicit. FY2025 was excluded before fitting because full-year payout qualification was not established.

The outcome is the change in the annual mean of qualified monthly discounts. Predictors are log growth in reported fiscal aggregate dividends and the change in preferred/common non-treasury share ratio. A fixed sensitivity substitutes split-normalized common DPS growth. This is a **retrospective same-year association**, with fourteen consecutive changes, FY2011–FY2024. Fiscal allocations are not calendar-year cash receipt dates; year-end supply is not average public float. Publication unknowns preclude using these rows as origin-available historical predictors.

All four fixed full-sample regressions used the same fourteen years:

| Design | Payout coefficient, pp per log unit of growth | HC1 t-based 95% interval | Nominal p | Fit R² |
| --- | ---: | --- | ---: | ---: |
| Supply-only | — | — | — | 0.0006 |
| Aggregate dividend growth only | −1.847 | [−8.107, +4.413] | 0.532 | 0.0193 |
| Aggregate growth + supply change | −1.865 | [−8.423, +4.694] | 0.544 | 0.0202 |
| Common DPS growth + supply change | −1.905 | [−8.413, +4.603] | 0.533 | 0.0213 |

Negative point estimates associate payout growth with narrowing, but intervals permit either sign. The two primary joint payout tests have **BH q=0.544**; they share the same data and are not independent confirmations. Fixed HAC1 inference is also weak: nominal p≈**0.489/0.478** for aggregate/DPS growth. HAC1 uses adjacent calendar years, small-sample correction and t intervals; the tiny annual sample makes all such uncertainty estimates fragile.

The known-special-year sensitivity excludes outcome years FY2020 and FY2021, thereby removing both the large special allocation and its reversal in growth. It retains twelve changes. The aggregate joint payout coefficient becomes **−3.958**, HC1 95% interval **[−12.982, +5.067]**, p≈**0.347**; no strong association emerges. Leave-one-year-out joint payout coefficients remain negative, ranging **−4.962 to −0.503**, but a stable sign is not a precise or causal effect.

The [complete coefficient table](LOOP_TREE_ANNUAL_PAYOUT_COEFFICIENTS_20261112.csv) includes every intercept/supply/payout term, both covariance conventions and the fixed sensitivity. No year was selected for omission because of its fitted loss or p-value.

### Which payout hypothesis has actually been tested?

The simple annual delivered-dividend/supply design does not explain much of the discount movement in this sample. That is a new scoped negative result. It does **not** rule out payout-policy credibility, investor composition, tax effects, intra-year announcement responses, actual public-float changes or effects measured on a different economically qualified design.

Preferred-minus-common annual DPS is exactly **KRW1 per post-split-equivalent share in all fifteen years**. Its stand-alone effect is not identified: a constant regressor cannot distinguish a class-cash mechanism from the intercept. This is a data-design limitation, not a zero estimated effect. The FCF denominator and repurchase cash remain unreconciled, so these regressions do not test compliance with the full FCF-return promise.

## Tree implications and remaining limits

| Branch | Progress from this batch | What remains open |
| --- | --- | --- |
| B01/B02 | Matching-memory anchor comparison completed across all declared price designs | Future stability and economic versus measurement origin of the anchor |
| B04 / scoped state information | Level/state regressions generally add little for Novo; a fixed activity exception retained | General nonlinear regimes not identified; no new link/window search |
| L01 activity proxy | Exact scoped five-year expanding Novo increment quantified | True liquidity/depth, signed demand and executable prices unobserved |
| P05/P01 | Annual delivered-payout association tested; weak fit and broad intervals | Credibility, class clientele, publication-time panel and causal intervention |
| S06 | Supply rival included on the identical new annual sample | Issued-minus-treasury is not public float; ownership/cost mechanisms unresolved |
| Differential cash rights | Identifying variation checked; constant in this panel | A qualified class-relative payout shock is still needed |

Governance/control shocks, signed retail/foreign/institutional flows, actual borrow inventory/fees, systematic grant/issuance events and synchronized auction/receipt/FX records are still not measured adequately for their intended tests. Regressing their names on price history would not answer those tree questions. All twenty pilot dates, sixty missing primary slots, held prehistory, provider denials and source-clock qualifications remain unchanged.

## Execution and independent verification

Fit job **15316412** completed in **1m14s**, exit0, maximum RSS about306MiB; independent verification job **15316459** completed in **22s**, exit0, about173MiB. Both used one CPU and explicit node/memory/time requests. No sustained work ran on the login node.

The verifier checked all **54,748 forecast cases**, all **524 aggregate rows** and all **26 annual coefficient/covariance rows**. An independent terminal-anchor identity differed by at most **4.27×10⁻¹⁴ pp**; independently reconstructed covariance standard errors differed by at most **1.82×10⁻¹²**. Saved source code, input hashes and thirteen original report hashes passed. Arithmetic verification is not a second economic sample.

Config: `configs/loop_tree_productive_batch_v1.json`; fitting and verification code: `scripts/run_loop_tree_batch_v1.py`, `scripts/verify_tree_productive_batch_v1.py`; private run: `runs/loop_long_horizon/tree_productive_15316412/`; source panel: ignored `data/acquisition/2026-11-12/productive_tree_regressions_v1/`. The executed source and config are copied in the run. The provenance shorthand `no_new_intervals_or_features` refers to unchanged monthly forecasting designs; new retrospective annual payout covariates are explicitly authorized and separately recorded, not historical forecast features. Private source rows and forecast origins remain out of public Git. Canonical historical statuses and old verdict scopes are preserved; new findings are attached separately.

Private delivery archive `productive_tree_regressions_2026-11-12_v1.zip`: **6,681,402 bytes; 52 files**, SHA-256 `f40d14d066815d95f793730780d56a455bf6ca389553a4ecf2521d12fd3bfb5d`. Separate full-inventory SHA-256 `562f3a591fac00cb618e2a75d272c8a9c75cec3dd52e8e1cc91e1a3ac078eb1d`; delivery JSON and SHA-256 sidecars are under ignored `data/acquisition/2026-11-12/`. Every archive entry size/hash and CRC passed. The archive contains source qualification, exact code/config, preserved pre-batch ledger/tree snapshots and the full fitted/verified run; public documentation alone does not transfer licensed inputs.
