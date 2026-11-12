# LOOP long horizon linear model results November 12 2026

The first batch produced results across all nine newly acquired comparisons. A universal linear correction model is not supported by this specification: the simplest model beats persistence in four of eleven evaluable class samples at two years and four of eleven at five years. Adding relative trading activity makes every evaluable two-year forecast comparison worse than the same-origin state model. Novo is the clearest preliminary repeat candidate across both horizons, but no predictive model is validated for prospective use.

Execution: Slurm job `15293344`, configuration `configs/loop_long_horizon_v1.json`, executed source committed at `17bd49f`. Private outputs: `runs/loop_long_horizon/15293344/`. Separate verification job `15293441` reconstructed all 13,695 forecasts with calendar-date training masks and independent numpy least squares; maximum prediction difference was 3.35e-12 percentage points. All 131 aggregate evaluation rows and source hashes passed. Five synthetic calendar, leakage, aggregation and durable-checkpoint checks passed. No separate agent review is claimed.

## What ran

Fourteen class-specific panels cover the nine comparisons. The batch estimated 203 of 252 predeclared sample/coverage/model/horizon combinations; blocked fits remain in the model-status table with their reasons. There are 13,695 overlapping retrospective forecast cases, not 13,695 independent experiments. The horizons are 24/60/120 calendar months, not two-, five- and ten-year lookback regressions. The forecast outcome is the change in the monthly mean observed price discount, not a required return or cash-inclusive trading payoff.

Public aggregate tables: [all forecast scores](LOOP_LONG_HORIZON_SCORECARD_20261112.csv), [same-origin nested comparisons](LOOP_LONG_HORIZON_INCREMENTAL_20261112.csv), [every fitted or blocked model](LOOP_LONG_HORIZON_MODEL_STATUS_20261112.csv), and [descriptive coefficients](LOOP_LONG_HORIZON_COEFFICIENTS_20261112.csv). Licensed monthly panels, individual forecast origins, and conditional future projections remain private.

## Discount state versus persistence

`LH-LEVEL` predicts terminal discount change using the current monthly discount and an intercept. Positive out-of-sample R-squared means lower mean squared error than zero-change persistence on identical origins. Negative values mean worse performance; these are loss comparisons on exposed history, not significance tests. Main coverage is pragmatic; strict coverage is an independently frozen cleaning sensitivity.

| Sample | 2-year forecasts | 2-year R2 main / strict | 5-year forecasts | 5-year R2 main / strict |
| --- | ---: | ---: | ---: | ---: |
| byd A H | 99 | -0.211 / -0.220 | 27 | 0.644 / 0.430 |
| hdfc local ADS | 178 | -0.339 / -0.381 | 106 | 0.054 / 0.042 |
| hyundai common local pref 1 | 173 | -0.367 / -0.365 | 107 | -1.832 / -1.863 |
| hyundai common local pref 2 | 173 | -0.389 / -0.384 | 107 | -1.651 / -1.688 |
| hyundai common local pref 3 | 163 | -0.812 / -0.840 | 91 | -5.917 / -6.461 |
| novo nordisk local ADS | 176 | 0.404 / 0.402 | 105 | 0.162 / 0.157 |
| ping an A H | 151 | -0.970 / -0.948 | 81 | -3.280 / -3.366 |
| roche voting Genussschein | 172 | 0.169 / 0.169 | 100 | -0.346 / -0.346 |
| shell RDS A | 115 | 0.349 / 0.349 | 43 | -0.890 / -0.890 |
| shell RDS B | 115 | 0.093 / 0.091 | 43 | 0.558 / 0.566 |
| volkswagen ordinary preferred | 179 | -7.208 / -7.208 | 107 | -0.076 / -0.076 |

The score signs agree under both coverage rules in all 22 estimable sample/horizon cases. Isolated cleaning differences therefore do not explain the main mixed result. Several state models are unstable, especially VW; those losses are retained rather than discarding unusual valid price periods to improve performance.

Novo improves at both horizons under both rules. Roche and the retired Shell A/B classes improve at two years, while the latter classes end in January 2022 and are not forecasts for unified Shell. BYD, HDFC, Novo and historical Shell B improve at five years. BYD has only 27 overlapping baseline origins at five years, at most one nonoverlapping holding period per phase, so the apparent gain is particularly weak evidence of transferability. Across the other samples, the maximum nonoverlapping counts are only 5–8 at two years and 1–2 at five years; monthly overlap cannot create additional economic episodes.

## Does relative activity add information

The state baseline contains current discount and trailing twelve-month discount change. The activity extension adds the relative volume proxy; each comparison uses exactly matched origins.

| Sample | 2-year activity incremental R2 | 5-year activity incremental R2 |
| --- | ---: | ---: |
| byd A H | -0.128 | -0.204 |
| hdfc local ADS | -0.056 | -0.060 |
| hyundai common local pref 1 | -0.202 | 0.136 |
| hyundai common local pref 2 | -0.119 | 0.119 |
| hyundai common local pref 3 | -0.335 | 0.296 |
| novo nordisk local ADS | -0.090 | 0.076 |
| ping an A H | -0.043 | 0.011 |
| roche voting Genussschein | -0.162 | 0.187 |
| shell RDS A | -0.032 | 0.047 |
| shell RDS B | -0.285 | -0.076 |
| volkswagen ordinary preferred | -2.196 | 0.129 |

Activity worsens all 11 two-year comparisons under both coverage rules. It improves 8/11 pragmatic five-year comparisons and 8/10 strict comparisons; one strict case lacks enough forecast history. Improving a weak state model does not necessarily beat persistence: for example, the Hyundai five-year activity models still lose to persistence. These results reject the claim that this volume feature reliably improves the frozen two-year design. They do not reject liquidity costs, supply, ownership or investor demand as economic mechanisms.

## What cannot be evaluated yet

No ten-year forecast survives the predeclared matured-label training/evaluation requirements, although 65 ten-year descriptive models can be fitted across the two coverage variants. This is insufficient evaluation history, not a null ten-year result. Short Alibaba, unified Shell and Roche participation histories also cannot support the declared retrospective forecast evaluation. Their failed or unestimated specifications are recorded; rows are not counted as null findings.

Current full-fit projections at 24/60/120 months are saved privately as unvalidated conditional linear candidates. Historical vendor vintages are unavailable and all prices are exposed; no untouched holdout or prospective validation is claimed. P-values are deliberately omitted from the long-horizon interpretation. HAC errors in the coefficient table are descriptive and can be misleading with persistent predictors and few independent spans.

## Measurement assumptions and durable progress

Isolated invalid days are excluded automatically; no future backfill or FX extrapolation is used. Monthly ratios precede averaging; exact calendar-month endpoints and missing months are preserved. Six ECB reference series covering the longer history were downloaded from the public ECB data API and frozen by hash, URL and retrieval time. Actual security/FX join losses are in the private coverage table. Same-date reference FX and unsynchronized closes define retrospective monthly gaps. They do not establish intraday parity or execution. Receipt ratios and historical Shell GBP scale retain the documented assumptions from the receipt review.

All raw snapshots and prior empirical runs remain unchanged. The original run stores source/input hashes and all complete aggregate results. The verification directory adds complete per-class recovery checkpoints and the exact executed source from commit `17bd49f`. The next-run engine now checkpoints actual per-variant results and monthly CSV contents during processing, rather than only completion markers; this improvement did not change or rerun these estimates.

## Hypothesis tree decisions and next discriminating work

- **M01/M02:** data now support scoped exploratory monthly models across all nine comparisons; retain structural boundaries and the unverified timing/ratio assumptions. Do not reopen global acquisition holds because a few rows are missing.
- **B01/B02:** universal discount-state correction is insufficient. Retain persistence in every comparison; prioritize regime/parameter stability and fixed train-only linear regularization before adding many predictors. Preserve the stronger Novo candidate without promoting it to a validated forecast.
- **L01:** retain the negative two-year activity result as a specification-specific finding. Five-year incremental signals remain tentative; investigate actual supply, float, ownership and costs rather than relabeling volume as liquidity.
- **S06, LH2–LH4:** the price-only batch cannot resolve public supply, ownership/control or payout credibility. Add independently dated mechanism histories to discriminate these branches; do not treat their absence as evidence against them.
- **Prospective validation:** a fresh future-origin cohort is needed for a deployable claim; ten-year accuracy cannot be established by recycling overlapping historical labels.

The [protocol](LOOP_LONG_HORIZON_PROTOCOL_20261112.md), [canonical tree](PREDICTION_MECHANISM_TREE.json), readable tree, execution ledger and append-only evidence ledger record this batch. Previous Samsung, US proxy, core-pair and daily findings remain scoped to their original data and horizons.
