# What we tested about related-security price gaps—and what the results establish

**Research evidence paper · November 12, 2026 · Existing estimates and bounded descriptive audits**

## Abstract

This project asks why securities tied to the same issuer or underlying business trade at different relative prices, whether those gaps predict subsequent adjustment, and whether an investor could capture that adjustment. Those are three separate questions. We find descriptive correction in several markets, heterogeneous historical forecast improvements, and important measurement and implementation limits. We have not established a universal predictor, an identified economic mechanism, or an executable arbitrage.

Samsung's locked primary forecast improved one-session mean absolute error by only **0.000725 percentage points**, with an uncertainty interval spanning zero. Its supply ratio explained annual levels much better than annual changes. Broader US comparisons showed the clearest short-horizon forecasting improvement for Berkshire; other apparent successes often depended on an easy benchmark. The long-horizon LOOP tests found historical improvement over persistence in **4 of 11** evaluable samples at both two and five years. Novo was the most consistent repeat candidate across fixed methods and training histories. Its level-only methods lost to a training-only terminal-discount mean in LH5; a broader matching-memory comparison now confirms that its level and state models lose under both expanding and rolling training. A five-year expanding OLS activity model is a scoped exception, reducing MSE against its matching anchor by **6.81% pragmatic / 5.11% strict**, but not surviving rolling training or ridge. Earlier forecast wins and this limited exception remain visible without establishing universal conditional information or prospective skill.

The evidence now supports a measurement-first Novo investigation and a registered future-origin test. Two subsequent bounded audits reconcile Samsung's reported cash delivery with specific policy commitments and show the large effect of Novo's December 2007 unit mismatch on daily comparator arithmetic; neither identifies a causal price mechanism. Twenty acquisition dates remain frozen, and all sixty synchronized pilot component slots remain missing. The **6,091 decoded FX rows are candidates**, not qualified observations. This paper synthesizes completed artifacts; it does not rerun estimation or change the canonical hypothesis verdicts. The [timeline](LOOP_SIMPLE_TIMELINE_20261112.md) is the condensed companion.

## 1. Questions, quantities and standards of evidence

For Samsung, the observed discount is `q = 100 × (1 − preferred/common)`. A positive change widens the gap; a negative change narrows it. Other comparisons use their own documented class/receipt ratios and currency conventions. The US exception study uses log relative-price changes. Holding-company return betas measure exposures. These outcomes are not interchangeable, and none is automatically a required-return discount rate, NAV discount or cash-inclusive portfolio return. [Methodology](METHODOLOGY.md), [US exceptions](LOOP_EXCEPTION_TEST_RESULTS_20261109.md), [long-horizon protocol](LOOP_LONG_HORIZON_PROTOCOL_20261112.md).

We distinguish four claims:

| Claim | Evidence needed | What this project currently has |
| --- | --- | --- |
| Prices move together or gaps subsequently correct | Defined prices, units, timing and an association | Several retrospective associations, with pair-specific measurement qualifications |
| A model predicts better than a benchmark | Same-origin loss comparison using only matured training labels | Some exposed-history improvements; no universal or prospective validation |
| A proposed mechanism causes the gap or correction | Independently measured mechanism and a design separating rivals | Proxy tests, descriptive cases and unresolved data gates |
| The relationship is profitable to trade | Executable prices, position/cash accounting, borrow, costs, timing and legal feasibility | Preliminary diagnostics; no certified executable arbitrage |

For forecast tables, `R² versus benchmark = 1 − model MSE / benchmark MSE`. Positive means lower historical squared forecast loss; negative means worse. This is not in-sample explanatory R² or a significance test. MAE gains have the opposite reporting convention: positive baseline MAE minus model MAE means improvement. One percentage point of discount change is not a one-percent investment return.

Three benchmarks matter: **persistence** predicts zero change; **mean historical change** predicts the average matured change; **terminal-level mean** predicts the average matured terminal discount minus today's discount. The last can predict a change without a fitted conditional slope. A model beating one benchmark need not beat another. The term “out of sample” in the archived scores means chronological pseudo-out-of-sample evaluation of exposed history; unavailable original vendor vintages and prior viewing preclude an untouched historical replay. [LH5 definitions](LOOP_LH5_MEAN_RESULTS_20261112.md).

For the tables below, **pp** means percentage points, **MAE** is average absolute forecast error, and **RMSE** is the square root of average squared forecast error, which puts more weight on large mistakes. **HAC** standard errors account for serial dependence and unequal error variance; **HC1** accounts for unequal error variance. A **BH q-value** adjusts a batch of significance tests for multiple comparisons. A small p-value or q-value does not establish economic importance, causation or profit.

The canonical [44-node tree](PREDICTION_MECHANISM_TREE.json) separates historical status from long-horizon status. Its `supported`, `contradicted`, `unresolved` and `untested` labels retain their original scope. In this paper, **unsupported/rejected design** means the particular tested design failed its stated comparison; it does not reject every mechanism associated with that branch. **Data-gated/not run** is not a null result. Legacy regression names B01–B04 are model labels and are not identical to the tree's B01–B04 benchmark hypotheses.

## 2. Samsung: statistical correction did not become a reliable primary forecast

### T01. Retrospective factor and gap regressions

**Question and method.** On the existing 2005–2026 Samsung observed-session history, B01 regressed discount changes on aligned US-Barra factors, B02 used log-gap changes, B03 added lagged discount, and B04 added lagged relative class activity. Fixed full/2005–2014/2015–2019/2020–2026 windows, main/sensitivity samples and HAC bandwidths 5/20/60 were retained. The archived coefficient inventory has 1,224 rows; these repeated specifications are not independent discoveries.

**Result.** Lagged-discount adjustment is visible: full-sample main B03 has coefficient about **−0.0043**, p=**4.47×10⁻⁶**, BH q≈**0.0002**. The full-sample B04 DIVYILD association is **25.646**, p≈**0.0249**, but BH q≈**0.1888**; activity's nominal p≈**0.0183** has q≈**0.1643**. Some sensitivity findings differ, so “nothing survives adjustment anywhere” would also be incorrect. The complete tables, rather than one favorable factor, define the evidence.

**Interpretation.** A US factor return is not Samsung's class dividend, investor flow or observed trading cost. Historical factor publication/revision times are unverified, and calendar alignment is a retrospective rule. These are explanatory associations, not causal mechanisms or deployable forecasts. Sources: [coefficient tables](B01_B04_RETROSPECTIVE_COEFFICIENT_TABLES.md), [methodology](METHODOLOGY.md), [analyst AR11](LOOP_ANALYST_REVIEW_20261112.md#ar11--dividend-factor-associations-do-not-establish-a-class-payout-mechanism).

### T02. Locked forecasting experiment

**Question and sample.** Could compact history predict 1/5/20-session discount changes better than zero-change persistence and direct AR? Initial training ended in 2014; development folds covered 2015–2017, 2018–2020 and 2021–2023; the locked evaluation covered 2024 onward, with targets through October 20, 2026. Monthly expanding refits used matured labels and training-only scaling. Candidate families included direct AR, latest-change/history and activity extensions; validation selected H1 ridge alpha 100. Activity did not earn promotion. Historical descriptions had already been viewed; “locked” does not mean all history was unseen.

| Horizon | Matched origins | H1 MAE | Persistence MAE | Direct AR MAE | H1 R² vs persistence |
| --- | ---: | ---: | ---: | ---: | ---: |
| 1 session, primary | 679 | 0.645551 | 0.646276 | 0.644646 | +0.002994 |
| 5 sessions | 675 | 1.280598 | 1.275236 | 1.267534 | +0.015515 |
| 20 sessions | 660 | 2.239976 | 2.114604 | 2.084507 | −0.112257 |

Errors are percentage points. The one-session MAE gain **0.000725** has block-20 95% interval **[−0.009182, +0.011332]**; direct AR's point estimate is better. Five-session MAE worsens even though its squared-error comparison is positive; twenty-session performance deteriorates. Main/strict evaluation coincides in this final sample, while earlier validation coverage differs.

**Decision.** No reliable primary-horizon improvement established; retain persistence. Conditional block intervals omit model-selection and re-estimation uncertainty. Six invalid paired dates remain missing, and the observed-session grid is not an independently verified exchange calendar. Source: [locked forecast report](PREDICTION_RESEARCH_REPORT.md).

### T03. Fixed continuation designs and diagnostics

Residual/regime/coverage/refit diagnostics motivated five bounded follow-ups. They used the same original proxy grid, label maturity rules and matched challenger/base samples. The primary gate required material development improvement and stability; no lag/window sweep followed failure. All 2024–2026 results below were already exposed.

| Fixed candidate | Primary comparison | Development MAE gain, pp | Development-fold wins | Exposed primary gain, pp | Scoped decision |
| --- | --- | ---: | ---: | ---: | --- |
| D1: intercept + latest change | Persistence | +0.009110 | 3/3 | +0.000606 | Development support; tiny uncertain primary transfer |
| R756: rolling level, fixed 756-origin window | Persistence | −0.000999 | 1/3 | −0.004095 | This rolling-level design unsupported |
| F4: delayed VIX/FX/rate state block | Matched reversal ridge base | −0.001305 | 0/3 | +0.000678 | Failed incremental development gate |
| G2: activity surprise/range difference | Same matched base | −0.000020 | 2/3 | −0.000584 | Failed materiality gate |
| C2: known late-quarter/year indicators | Same matched base | −0.000266 | 1/3 | −0.000749 | No material primary calendar increment |

D1's five-session MAE gain is **0.016738 pp**, block-20 interval **[0.001545, 0.034861]**, versus persistence. It is a secondary, adaptively motivated result on viewed outcomes—not confirmation. Its primary interval crosses zero. D1's descriptive slopes are negative at all three horizons, but that association does not establish stable forecast skill. F4 used conservative delayed current-vintage public data, not verified original release vintages; G2 is activity/range, not liquidity or signed flow; C2 is generic calendar, not an actual dividend event test. Final coefficient/future-readiness archiving issued no historical or future forecast. Source: [continuation report](PREDICTION_CONTINUATION_REPORT.md).

## 3. Samsung: supply, price-leg and issuer-event tests

### T04. Long-horizon map and annual supply/activity

The descriptive map contains **261** qualified complete months, January 2005–September 2026, and **87** complete quarters. Endpoint comparisons at 24/60/120 months number **237/201/141**, but the single-anchor nonoverlapping counts are only **10/4/2**. This describes persistent discount states; it is not a forecast test or cash-inclusive return. Last-valid quote labels and staleness were explicitly reviewed. [Independent long-horizon inspection](LONG_HORIZON_INSPECTION.md).

The annual mechanism test used **17** joint level observations (2005 and 2010–2025) and **15** consecutive changes (2011–2025), with HC1 OLS, permutation and rank checks. Supply-only levels have R² **0.6984**; the joint supply/activity/time level model has R² **0.7025**, but supply's partial permutation p becomes **0.0921** and activity's **0.6517**. The joint first-difference R² is **0.0006**, with p≈**0.9864/0.9316** for supply/activity. During 2018–2023 the measured non-treasury ratio is effectively constant while the discount spans **9.61 points**.

**Decision.** Simple non-treasury supply alone is insufficient to explain the observed movements. Levels describe regimes more strongly than changes. This does not reject public-float, ownership or true transaction-cost mechanisms: issued minus treasury is not verified public float, and activity per year-end shares is not trading cost. Sources and unit conflicts remain explicit. [Hypothesis-resolution H1](HYPOTHESIS_RESOLUTION_RESULTS_20261109.md#h1--samsung-supply-versus-trading-capacity).

### T05. Which price leg adjusts?

Adjusted forward common, preferred and preferred-minus-common log returns were regressed on a one-point current discount widening at fixed 1/5/20-session horizons, excluding missing/flagged intervals without bridging. Preferred-over-common correction is about **0.14% / 0.38% / 0.53%**, with low adjusted R² **0.0110/0.0222/0.0175**. Preferred catch-up is positive at all three horizons; common reversal is distinguishable from zero only at five sessions in the full sample. Signs persist across the fixed subperiods.

**Decision.** Preferred catch-up is the descriptive price-leg channel. Investor identity, stale quotes, auction effects, bid–ask bounce and executable reversal remain unresolved. Exploratory, dependent-horizon p-values are not multiplicity-adjusted. [Hypothesis-resolution H2](HYPOTHESIS_RESOLUTION_RESULTS_20261109.md#h2--which-samsung-share-class-adjusts-after-a-widening).

### T06. Buyback authorization, execution, cancellation and dividend cases

Six disclosures represent **three connected clusters**, not six independent events. Conservative next-observed-session windows were fixed at 1/5/20 sessions; exact publication clocks are unknown. The 2024/2025 authorization doses were almost class-proportional. Twenty-session changes after 2024 authorization/execution/cancellation were **+2.34/−1.00/+1.10 pp**; after 2025 authorization/execution they were **+1.20/+1.90 pp**. Positive means widening. The FY2024 KRW363 common/KRW364 preferred dividend decision had mixed **−0.20/+0.22/−0.61 pp** windows.

**Decision.** These cases do not identify preferred-relative issuer support as the cause of narrowing. Execution-report dates are not historical purchase dates; cancellation of already-held treasury is not a second market purchase. Connected stages, anticipation and policy endogeneity limit inference. Employee grants, issuance/conversion shocks and a repeated origin-qualified payout panel were not tested. [Hypothesis-resolution H3](HYPOTHESIS_RESOLUTION_RESULTS_20261109.md#h3--recent-repurchase-cancellation-and-dividend-disclosures).

## 4. Generalization: related markets behave differently

### T07. Three core-pair price baselines

HAC(20) B00 regressions tested lagged gap adjustment on the inherited exact price panels through November 6, 2026. These are in-sample price associations, not NAV or forecast tests.

| Pair | Actual sample | n | Lag-gap coefficient | p | Adjusted R² |
| --- | --- | ---: | ---: | ---: | ---: |
| SK Square / SK Hynix | 2021-11-30–2026-11-06 | 1,149 | −0.01153 | 0.0084 | 0.56% |
| Samsung Fire / Samsung Electronics | 2005-01-04–2026-11-06 | 5,203 | −0.00148 | 0.130 | 0.06% |
| TSMC local / ADR | 2005-01-04–2026-11-06 | 4,737 | −0.06905 | 4.15×10⁻²⁰ | 3.42% |

Korean NAV regressions remain data-gated by dated ownership/valuation histories. The TSMC baseline's same-date noon-New-York FX occurs after Taiwan closes, so it is retrospective. ADR continuation tags, action rows and missing quotes remain preserved; no assumed historical source clock is upgraded by matching identifiers. [Core-pair report](CORE_PAIR_BASELINE_RESULTS.md).

### T08. TSMC timing decomposition

Separate clock definitions asked which venue moves toward parity: Taiwan-close state → later US ADR return, and US-close state → next Taiwan-local return. Full-sample HAC(5) coefficients are **−0.04510** (n=5,407; adjusted R² 1.52%) and **+0.06116** (n=5,359; 4.45%). Signs survive the fixed ADR-spread sensitivity and fixed subperiods. The 2015–2019 coefficients are much stronger, about **−0.371/+0.390**.

**Decision.** Both venues participate in measured adjustment; no one-market-only story fits this design. Stronger middle-period adjustment is an anomaly to preserve, not a selected break or causal regime. Daily fixing/timing definitions, absent local executable quotes and conversion/borrow costs prevent an arbitrage interpretation. [Hypothesis-resolution H4](HYPOTHESIS_RESOLUTION_RESULTS_20261109.md#h4--tsmc-cross-market-price-discovery).

### T09. Prosus/Tencent/Naspers exposure and local gap models

The exact-interval return study used documented local securities converted to USD, identical interval endpoints, common samples, adjustment/action exclusions, fixed stock-only/market/factor designs, action-window and one-interval-lag sensitivities, and rolling summaries. Its configured period is September 11, 2019–September 30, 2026. Prosus/Tencent's stock-only beta is **0.736** (n=1,609), falling to **0.637** with regional controls; Naspers/Prosus stock-only beta is about **0.971**. Contemporaneous exposure is strong, while the archived analyst review finds weak lag signal. Return-basis and action-window qualifications survive.

A separate normalized local price-gap/factor model has 1,841 common dates, 1,734 usable levels and 1,611 full-model observations. Full-window adjusted R² is only **0.48%–0.71%**. B03's lagged gap has nominal p=**0.0183** but BH q≈**0.634**; no factor finding survives that batch's adjustment, and activity does not add support. Older windows are blocked by actual coverage.

**Decision.** Strong stock exposure coexists with weak gap explanation. Neither exposure betas nor normalized first-price ratios establish historical NAV or a cheap claim. Dated holdings, other assets/liabilities, taxes, share counts and cash-distribution bases remain necessary. Sources: [return specification](../../configs/prosus_tencent_return_regressions.v1.json), [analyst AR10](LOOP_ANALYST_REVIEW_20261112.md#ar10--prosus-naspers-and-other-holdco-betas-are-exposures-not-nav-convergence), [local gap H8](LOOP_EXCEPTION_TEST_RESULTS_20261109.md#h8--does-the-samsung-style-factorgap-design-transfer-to-prosustencent), [aggregate artifact inventory](LOOP_ANALYST_REVIEW_INVENTORY_20261112.csv).

### T10. Seven US pairs: correction and forecast benchmarks

The US study tested B00 correction and expanding forecasts after a 252-observation minimum. Seven pairs had 1,741–6,257 usable regression changes; forecast counts are below. Every model beat the aggressive next-level-to-prior-median forecast. Only Berkshire and narrowly Liberty beat zero-change persistence.

| Pair | In-sample correction at conventional p<0.05? | Forecast n | B00 / persistence RMSE | Forecast decision |
| --- | --- | ---: | --- | --- |
| Alphabet A/C | No | 2,736 | 0.1893 / 0.1892 | Loses to persistence |
| Berkshire A/B, post-2010 split | Yes | 3,791 | 0.2600 / 0.2692 | Best improvement, about 3.4% RMSE |
| News B/A | Yes, tiny fit | 2,932 | 0.4332 / 0.4330 | Loses |
| Fox B/A | Yes, tiny fit | 1,489 | 0.3293 / 0.3278 | Loses |
| Liberty Broadband A/C | Yes | 2,527 | 0.2626 / 0.2631 | Very small improvement, about 0.2% |
| Petrobras common/preferred ADR | Yes, tiny fit | 6,005 | 0.7600 / 0.7599 | Loses |
| Volkswagen ADR proxy | No | 5,427 | 2.7546 / 2.6625 | Loses substantially |

**Decision.** Correction generalizes statistically to some pairs, but useful historical prediction is much less general. Different voting/cash/depositary rights mean zero gap is not universally fair value. These USD proxy listings do not silently replace exact local class or venue tests. [US H1–H2](LOOP_EXCEPTION_TEST_RESULTS_20261109.md).

### T11. US legs, liquidity proxies, strategy diagnostics, holdcos and common factor

The remaining frozen US tests addressed distinct questions:

| Test | Sample/design | Result | What remains unresolved |
| --- | --- | --- | --- |
| Which leg follows a widening? | 1/5/20-session event descriptions across seven pairs | Relative correction after widening; cheaper/right leg generally catches up. Small Alphabet/Liberty/Fox event counts limit conclusions. | Causal price discovery and executable entry |
| Do spreads/turnover mismatch explain deviations? | HAC(20), deviations from prior 252-session median; six estimable quote histories | Positive spread association for Alphabet, Berkshire and Petrobras; opposite sign for News; mixed turnover signs. VW quotes absent. | Universal liquidity-cost mechanism; absence is not zero cost |
| Does a fixed z-score diagnostic look promising? | Prior-information 252-session z-score, threshold 1, next ratio change, observed half-spread turnover charge | Six quoted pairs have positive quote-net annualized log-score means; reported net Sharpes 0.27–1.58. | Borrow, cash/dividends, funding, conversion, impact and legal execution; no portfolio performance certified |
| Holdco return pass-through | Six contemporaneous heldco-return regressions, downside interaction, HAC(20) | Up betas: Liberty/Charter 0.878; BN/BAM 0.817; SoftBank/Arm 0.401; Prosus/Tencent 0.794; Naspers/Prosus 1.006; Investor/Atlas 0.246. Conventional downside asymmetry only Liberty and SoftBank. | Dated NAV and convergence; proxy exposure is not cheapness |
| One global gap factor? | PCA on 1,662 complete US dates; exact-calendar core-pair correlations | PC1 explains **16.22%**, mixed loadings and generally small cross-market correlations. | Regional/rights-matched or stress-conditioned channels; asynchronous closes |

Sources: [US H3–H7](LOOP_EXCEPTION_TEST_RESULTS_20261109.md). The original VW gross drawdown label was dimensionally wrong: **−238.1755 log points** translates to about **−90.7612%** for the diagnostic geometric index under the same legacy peak convention, not financed portfolio wealth. Missing quote-net VW results stay missing. Berkshire's conversion direction, short-sale/funding assumptions and actual fills remain required implementation tests. [V4 unit audit](LOOP_LONG_HORIZON_V4_RESULTS_20261112.md), [analyst AR01–AR02](LOOP_ANALYST_REVIEW_20261112.md).

## 5. Two- and five-year forecasting: successes, failures and a harder benchmark

### T12. LH1: common linear correction and activity increments

**Question and design.** Fourteen class-specific panels across nine acquired comparisons used monthly mean price ratios and 24/60/120-calendar-month outcomes. Three short histories could not support evaluation: Alibaba, unified Shell and Roche participation. Eleven class samples had two-/five-year evaluation. Expanding training used only matured labels; pragmatic/strict cleaning was fixed independently. Unsynchronized closes, reference FX and historical ratio/scale assumptions define the observed monthly gaps.

The simplest level model forecasts discount change from current discount and an intercept. Pragmatic R² versus persistence is reported for every evaluable class, preserving losses:

| Comparison | 24m origins | 24m R² | 60m origins | 60m R² |
| --- | ---: | ---: | ---: | ---: |
| BYD A/H | 99 | −0.211 | 27 | +0.644 |
| HDFC local/ADS | 178 | −0.339 | 106 | +0.054 |
| Hyundai common/preferred 1 | 173 | −0.367 | 107 | −1.832 |
| Hyundai common/preferred 2 | 173 | −0.389 | 107 | −1.651 |
| Hyundai common/preferred 3 | 163 | −0.812 | 91 | −5.917 |
| Novo local/ADS | 176 | +0.404 | 105 | +0.162 |
| Ping An A/H | 151 | −0.970 | 81 | −3.280 |
| Roche voting/Genussschein | 172 | +0.169 | 100 | −0.346 |
| Historical Shell A | 115 | +0.349 | 43 | −0.890 |
| Historical Shell B | 115 | +0.093 | 43 | +0.558 |
| Volkswagen ordinary/preferred | 179 | −7.208 | 107 | −0.076 |

The score signs agree under strict cleaning in all 22 cases. There are **4/11** persistence wins at each horizon, with different winners. Novo wins both; BYD's large five-year value rests on only 27 overlapping origins and at most one nonoverlapping outcome per phase. Historical Shell classes end in January 2022; their results do not forecast unified Shell.

The activity extension adds a relative-volume proxy to current level and trailing 12-month change on identical origins. It worsens **all 11 two-year comparisons** under both cleaning rules; at five years it improves **8/11 pragmatic and 8/10 strict** state comparisons. Improvement over a weak state model does not necessarily beat persistence. This rejects universal two-year incremental value for that frozen activity design, not the economic liquidity mechanism. Source: [LH1 report and full tables](LOOP_LONG_HORIZON_RESULTS_20261112.md).

### T13. LH2–LH3: fixed regularization and training memory

LH2 fixed lambda=1 ridge before execution; no penalty was selected from evaluation losses. LH3 fixed a 120-calendar-month rolling origin history, with otherwise unchanged features and matured-label rules. Expanding comparisons were matched to successful rolling origins. **Eight** strict Ping An five-year activity origins failed the minimum training size and remain failures, not null forecasts.

| Level-model method/window | 24m persistence wins, pragmatic / strict | 60m persistence wins, pragmatic / strict |
| --- | --- | --- |
| Expanding OLS | 4/11 / 4/11 | 4/11 / 4/11 |
| Expanding fixed ridge | 6/11 / 6/11 | 3/11 / 3/11 |
| Rolling OLS | 3/11 / 3/11 | 4/11 / 4/11 |
| Rolling fixed ridge | 5/11 / 5/11 | 4/11 / 5/11 |

Novo stays positive in all four method/window combinations at both horizons. Its pragmatic rolling level OLS persistence R² is **0.396/0.136** at two/five years; ridge is **0.283/0.126**. Against the rolling mean of past changes, rolling OLS reduces MSE by about **44%/21%**. Those are real reported historical loss improvements; they are not prospective skill. VW remains adverse: rolling OLS persistence R² **−7.416/−0.097**, ridge **−1.609/−2.401**. No unusual valid period was deleted.

Five-year nonoverlap phases often contain only one or two outcomes; two-year phases have few spans and share data. Phase/period checks are dependence-aware diagnostics, not independent replications. Activity findings vary with shrinkage and memory, preserving rather than erasing LH1's scoped negative result. Sources: [LH2](LOOP_LONG_HORIZON_V2_RESULTS_20261112.md), [LH3](LOOP_LONG_HORIZON_V3_RESULTS_20261112.md), [complete LH3 scores](LOOP_LONG_HORIZON_V3_SCORECARD_20261112.csv).

### T14. LH4: support, benchmark and drawdown diagnostics, without refitting

The saved-output audit retained **524** score rows and **54,748** forecast-variant cases. It found **316** OLS cases with implied terminal q≥100, incompatible with a positive price ratio; these were forecasts, not observed negative prices. No saved ridge case breached the bound. It also found **161/524** score rows beating the training-mean benchmark while losing to persistence. For VW's pragmatic five-year expanding level OLS, R² is **−0.0759** versus persistence but **+0.8692** versus the historical mean; that mean's MSE is about **8.226 times** persistence MSE.

VW's largest two-year level-loss origin cohort is 2011, about **40.8%** of expanding squared loss. This prevents blaming all losses on the 2008 squeeze without a training/origin/target decomposition. Unit translation corrected the legacy log-drawdown interpretation described in T11. No predictions were clipped, bad-looking origins removed, models reestimated or post-hoc winner deployed. Independent arithmetic verification is a software check, not fresh market evidence. [LH4 results](LOOP_LONG_HORIZON_V4_RESULTS_20261112.md).

### T15. LH5: positive conditional mean versus a terminal anchor

LH5 registered one challenger: for positive ratio R, `E[R(t+h)|R(t)] = exp(a + b log R(t))`, estimated with a continuous-response quasi-mean objective. This enforces positive support; it is not exponentiated log-OLS, a count model, or a silent replacement of the linear experiment. All **5,026** eligible original level-model origins fit successfully; no new intervals/features entered. Original expanding OLS/ridge remained visible and all methods used identical matured rows and three benchmarks.

For Novo, all twelve method/horizon/coverage comparisons lose to the **terminal-level mean**:

| Horizon and coverage | OLS R² vs terminal anchor | Ridge | Positive conditional mean |
| --- | ---: | ---: | ---: |
| 24m pragmatic | −0.01138 | −0.17382 | −0.01148 |
| 24m strict | −0.01544 | −0.16394 | −0.01557 |
| 60m pragmatic | −0.03033 | −0.01438 | −0.03030 |
| 60m strict | −0.01948 | −0.01329 | −0.01945 |

The positive-mean candidate still beats persistence for Novo, pragmatic R² **0.40427/0.16229**. Across the full universe it has the same 4/11 persistence-win counts as OLS at each horizon. Therefore, LH5 does **not** erase observed predictability against persistence or prove pure measurement artifact. It shows no demonstrated incremental fitted-slope value beyond that expanding terminal anchor in the specified comparisons. It did **not** test a rolling-window terminal mean. Positive support fixes a mathematical defect; it is not itself improved prediction. [LH5 report](LOOP_LH5_MEAN_RESULTS_20261112.md), [all 132 scores](LOOP_LH5_MEAN_SCORECARD_20261112.csv).

No ten-year forecast evaluation is available under the declared matured-label requirements. Fitting ten-year descriptive models is not testing their prediction. The rolling-120-month sensitivity is especially unable to supply enough matured ten-year labels; this does not prove that independently qualified longer expanding histories could never do so.

## 6. What acquisition has advanced—and what has not been tested

### T16. Evidence receipt, interval admission and synchronized measurement

The five original bundles were verified and installed without overwriting differing snapshots. By LH4, the cited registry retained **1,991** facts, **1,981** with unknown first-publication dates; it admitted **zero structural forecast features and zero new backward paired intervals**. Integrity and transcription/coverage checks do not certify that every fact was available at old forecast origins or that every old quote came from the stated historical venue. [LH3 evidence gates](LOOP_LONG_HORIZON_V3_RESULTS_20261112.md), [LH4 evidence audit](LOOP_LONG_HORIZON_V4_RESULTS_20261112.md).

The Novo pilot fixes December 3–7, 2007; March 3–7, 2014; November 1–3 and 6–7, 2023; and March 3–7, 2025. The original frozen calendar manifest remains authoritative, with provider-calendar qualifications and historical DST. Twenty dates × auction/NYSE quote/FX quote = **sixty primary slots**, all still missing. The unchanged compressed public FX hour yields **6,091 candidate decoded rows**. Independent ORC byte-slice decoding reproduced every supplied raw field and candidate scale/time output: decompression gives 121,820 bytes; offsets run from 50 to 3,599,753 milliseconds, uniquely and increasingly; quote candidates are positive/noncrossed and volumes finite/nonnegative. These are structural checks, not historical schema qualification. Generic field/scaling documentation has not established a matched source-native export validating historical USD/DKK scale, direction, hourly origin, clock semantics and edition. Ages and eligibility remain unknown until actual Copenhagen auction events and validated quote clocks exist; the later rule is last eligible quote at or before event, maximum age 60 seconds.

WRDS Daily/Monthly TAQ subscription denials remain observed denials. Nasdaq/LSEG access remains unverified. December 2007 requires pre-INET Copenhagen records. The 1997 unit-transition caution, separate 2000 demerger/2001 basis gates, asynchronous December 2007 local/ADR splits and announced depositary conversion suspension remain explicit, with issuer/vendor date disagreements preserved. Issuer notices and current listing codes do not certify the quote feed underlying inherited Compustat prices. [Measurement checkpoint](LOOP_NOVO_MEASUREMENT_CHECKPOINT_20261112.md), [ORC audit](LOOP_NOVO_ORC_STORAGE_AUDIT_20261112.md), [local collection checkpoint](LOOP_NOVO_LOCAL_COLLECTION_CHECKPOINT_20261112.md).

**Current ORC receipt qualification:** the original new supplement ZIP is now fully verified: **561,548 bytes, 76 entries**, matching trusted archive and separate-inventory hashes, all entry sizes/hashes, CRC, safe-path/duplicate/symlink checks and extracted hashes. This supersedes the initial incomplete loose-file condition; that recovery history belongs in the receiving work log. The finalized pilot and five previously verified bundles retain their earlier status. Decoder candidates are not promoted into primary observations by either packaging or structural decoding. The [independent receiving audit](LOOP_NOVO_LOCAL_ORC_REVIEW_20261112.md) records this validation and the new private review receipt.

### T17. Prospective validation is registered, not run

The preissuance registry reserves twelve future feature months, December 2026–November 2027. Primary contrast: Novo terminal anchor versus persistence at 24 months, with independently eligible issued origins; conditional models, strict coverage, other classes and 60/120-month horizons remain secondary. No future forecast has been issued and no prospective outcome is available. Source delivery, identity, actual availability and positive-support gates must pass before issuance. This is a plan, not a completed predictive test. [Prospective registry](LOOP_PROSPECTIVE_REGISTRY_20261112.md), [active plan](LOOP_ACTIVE_RESEARCH_PLAN_20261112.md).

### T18. Samsung payout commitments versus reported delivery

The bounded P05 audit reviewed seven identified pages from existing FY2015–FY2021 reports, transcribed six FY2015–FY2020 dividend outcomes, and reconciled ten later-vintage comparisons. Reported aggregate dividends are **KRW3.068737/3.991892/5.826302/9.619243/9.619243/20.338075 trillion**, respectively. Pre-2018 class DPS is normalized by the documented 50-for-1 split in a separate comparison column; preferred annual cash exceeds common by **KRW1 per post-split-equivalent share** in every selected year.

Specific reported cash amounts are consistent with the dated rounded commitments. Importantly, FY2018's doubling used an initially announced FY2017 base of about KRW4.8 trillion; FY2017 was subsequently increased to about KRW5.8 trillion. The actual FY2018-over-final-FY2017 increase of about **65.1%** is therefore not a failed doubling test. FY2020 includes a special dividend; its own report was subject to AGM approval, while the FY2021 report later says the regular and special dividends were paid. Fiscal allocations, proposals and later payment confirmation remain separate.

**Decision.** A cash-delivery audit is now completed. Policy-defined FCF compliance, differential investor demand, credibility and causal effects on the class discount remain untested; no P05 historical status changes. Reported net-income payout ratios cannot certify FCF commitments. [Protocol](BOUNDED_PAYOUT_SPLIT_PROTOCOL_20261112.md), [full cash table, vintage checks and qualifications](BOUNDED_PAYOUT_SPLIT_RESULTS_20261112.md#1-samsung-reported-dividends-are-consistent-with-the-specific-cash-commitments).

### T19. Novo December 2007 split/conversion case

The fixed December 3–7 daily case reuses ten existing source price rows and ten daily ECB reference observations. With raw local close L, ADR close A and daily USD-per-DKK reference F, compare `A/(k×L×F)` for k=1 and the source-motivated k=2. The five-date aggregate ratio range changes from **1.9933–2.0345** to **0.9967–1.0173**. The discount range changes from **−103.455 to −99.333 pp** to **−1.727 to +0.333 pp**. Factor two follows the separate split trading clocks; it was not selected from the gap.

**Decision.** The unit mismatch can dominate apparent daily mispricing. This does not certify historical raw adjustment semantics, exact venue, legal conversion, residual fair value or synchronized prices, or establish an error in the original forecasting panel. All five dates share the mismatch and announced conversion suspension, so the case cannot isolate a causal suspension effect. The issuer/vendor December distribution/payment disagreement, unknown clocks and all sixty missing primary slots remain preserved. X03 gains a descriptive case, not a supported friction-effect verdict. No price series or forecast result was revised. [Full case, chronology and limits](BOUNDED_PAYOUT_SPLIT_RESULTS_20261112.md#2-novo-the-split-unit-mismatch-can-dominate-the-apparent-daily-gap).

### T20. Matching-memory terminal anchors across all existing price designs

The user-authorized productive batch refit every successful LH3 level/state/activity OLS and fixed-ridge forecast with the original expanding or rolling120 matured training rows, then supplied a terminal-level mean from those identical rows. All **54,748 forecast-method cases** reproduce saved predictions within **2.85×10⁻¹⁴ pp**. The new comparison retains **524 score rows**, all calendar/nonoverlap diagnostics, eight inherited failed origins and the original support breaches. It adds a benchmark, not a new feature/window search.

All sixteen Novo level-model comparisons and all sixteen state-model comparisons lose to their matching anchors. The missing rolling-anchor test therefore supports the earlier level-model ordering. A specific exception remains: five-year expanding activity OLS wins by **6.81%/5.11%** in pragmatic/strict coverage, with **88/74** origins, and beats level OLS by **5.46%/4.12%** on matched origins. Calendar-bucket aggregate scores are positive, but available nonoverlap phases contain only one or two outcomes, with just **31/60** and **28/54** phases beating the anchor. The win does not survive ridge or rolling training; it is a scoped historical activity-proxy candidate, not true liquidity causality or an automatically issued future forecast. Across the universe, all losses and heterogeneous wins remain in the full scorecard.

**Decision.** Preserve the limited activity exception while retaining the strong terminal-anchor rival for Novo's simpler models. No universal model or causal state mechanism is established. [Frozen protocol](LOOP_TREE_PRODUCTIVE_BATCH_PROTOCOL_20261112.md), [full findings and 524 scores](LOOP_TREE_PRODUCTIVE_BATCH_RESULTS_20261112.md#a-the-missing-terminal-anchor-comparisons).

### T21. Annual delivered payout versus discount changes, controlling measured supply

The same batch extends the reviewed cash panel to **fifteen FY2010–FY2024 levels**, yielding **fourteen FY2011–FY2024 changes**. Fixed supply-only, payout-only, joint aggregate-dividend-growth and joint common-DPS-growth regressions use identical years. This is retrospective same-year association, not origin-available forecasting or a policy intervention.

The aggregate joint payout coefficient is **−1.865 pp per log unit of dividend growth**, HC1 t-based 95% interval **[−8.423,+4.694]**, p=**0.544**, R²≈**0.0202**. The DPS sensitivity is similarly weak; the two primary joint payout terms have **BH q=0.544**. Fixed HAC1 and the predeclared exclusion of FY2020/FY2021 special-allocation/reversal outcomes do not establish an association. Leave-one-year-out signs remain negative but are not evidence of a precise or causal effect.

**Decision.** The simple annual payout/supply design explains little of this sample's gap changes. P05 credibility/clientele effects remain untested causally. Preferred-minus-common annual cash is a constant **KRW1 per post-split-equivalent share in all fifteen years**; its separate effect is not identified, rather than estimated as zero. Independent QR/covariance/source checks passed. [All coefficients, sensitivities and source qualifications](LOOP_TREE_PRODUCTIVE_BATCH_RESULTS_20261112.md#b-samsung-delivered-cash-supply-and-annual-discount-changes).

## 7. Every node in the hypothesis tree

The appendix below covers all **44 canonical nodes**. “Tested proxy” or “descriptive” does not upgrade a mechanism. Canonical statuses are copied in their historical scope; long-horizon and acquisition qualifications remain separate. T identifiers refer to the evidence sections above, whose links point to the original reports and full tables.

| Node | Hypothesis | Canonical historical status | What has actually been tested / result | Remaining status and evidence |
| --- | --- | --- | --- | --- |
| S06 | Cumulative supply / liquidity feedback | unresolved | T04 levels/change/stable-count tests; T21 matched annual payout/supply regression weak | Simple measured-supply design insufficient; public float/ownership/cost channel unresolved |
| S01 | Relative buyback authorization dose | unresolved | T06 nearly proportional 2024/2025 doses and mixed event paths | Sparse connected descriptions; persistent causal effect not established |
| S02 | Actual repurchase execution | unresolved | T06 report-window descriptions, narrowing in 2024 and widening in 2025 | Actual daily purchases/publication clocks not identified |
| S03 | Treasury cancellation versus float | unresolved | T06 mixed cancellation window | Same program, not independent demand; mechanism unresolved |
| S04 | Employee treasury grants/disposal | untested | No qualified grant/lockup/selling test | Not run; dated quantities and restrictions needed |
| S05 | Class issuance/float/conversion rights | untested | No qualified issuance/conversion shock test | Not run; rights and dated action evidence needed |
| L01 | Relative spread/depth premium | unresolved | T03/T04/T11 proxy findings scoped; T12–T13 heterogeneous increments; T20 limited five-year expanding Novo activity win beyond anchor | True costs/depth mechanism untested; no universal activity or execution claim |
| D01 | Retail clientele/individual imbalance | untested | Volume proxies tested, investor identity not observed | Not run; signed class demand needed |
| D02 | Foreign class allocation | untested | T03 delayed FX state block failed; not a foreign-flow test | Not run as demand mechanism |
| D03 | Institutional benchmark demand | untested | No dated benchmark/flow intervention | Not run; ownership and event timing needed |
| D05 | Income clientele/tax | untested | T01 factor yield association and T06 payout case do not identify holders/tax | Not run as clientele mechanism |
| D04 | Attention/sentiment | unresolved | T02–T03 history/activity proxies do not identify sentiment | Mechanism untested; independent demand/attention evidence needed |
| G01 | Common votes/control contest | untested | T11 cross-pair prices are not a control experiment | Not run; actual pivotal-vote episode needed |
| G02 | Minority protection/private benefits | untested | No qualified reform design | Not run |
| G04 | Cash protection versus effective minority votes | untested | No separately measured governance intervention | Not run; firm-wide and class-relative effects must separate |
| G03 | Contingent preferred voting rights | untested | T16 current rights checks are not trigger tests | Not run; actual historical trigger needed |
| P05 | Durable payout-policy credibility/delivery | untested | T18 delivery audit; T21 fifteen-year cash panel, fourteen annual-change payout/supply regressions weak | Causal credibility/clientele and independent FCF compliance untested; no causal status upgrade |
| P01 | Differential announced cash rights | unresolved | T06 one decision case; T21 class cash difference constant across fifteen years | Separate effect not identified here; qualified class-relative shock/announcement test needed |
| P02 | Common cash news/differential clientele | untested | No isolated class allocation response design | Not run |
| P04 | Payout uncertainty/noncumulative claim | untested | Rights foundation differs from a payout-uncertainty shock | Not run; no generic senior-fixed-coupon interpretation |
| P03 | Known payout calendar | unresolved | T03 C2 generic seasonality failed increment | Actual payout-calendar mechanism untested |
| S07 | Class unification/rights equalization | untested | Structural transitions preserved in T12/T16, no Samsung causal test | Not run; legal path and dated implementation needed |
| X01 | Same-class GDR/local parity | untested | T07–T08 TSMC comparisons exist; Samsung receipt parity not tested; T16 Novo pilot missing | Samsung mechanism untested; historical ratios and synchronized records gated |
| X02 | Cross-market discovery | untested | T08 TSMC both-venue correction; not a Samsung GDR result | Samsung mechanism untested; Novo event/quote clocks missing |
| X03 | Depositary friction/segmentation | untested | T16 contract/fee/suspension evidence; T19 five-date split/conversion case shows large candidate-unit arithmetic effect | Friction effect not identified; exact units/legal conversion and synchronized clocks remain gated |
| L02 | Borrow scarcity/fees | untested | T11 strategy screens omit actual borrow | Not run; availability, fees and locate histories needed |
| L03 | Short-sale rules/eligibility | untested | No qualified class-relative rule shock test | Not run; rule dummy is not fee evidence |
| L04 | Funding risk/arbitrage capital | unresolved | T11 strategy and T14 risk-unit diagnostics do not measure capital constraints | Mechanism untested; funded implementation absent |
| L05 | Short transactions versus positions | untested | No qualified transaction/position/fee distinction test | Not run |
| R01 | Global risk appetite/class allocation | unresolved | T01 factor associations, T03 failed delayed block, T11 weak common factor | Broad class-demand channel untested; proxy evidence scoped |
| R02 | Semiconductor/earnings information | untested | T01 sector factor does not isolate class reception | Mechanism not run |
| R03 | KRW risk/foreign clientele | unresolved | T03 delayed FX state failed incremental gate | Foreign allocation mechanism not run |
| R04 | Rates/income valuation | unresolved | T01/T03 yield/rate proxies do not identify class funding/clientele | Mechanism not run |
| R05 | Stress-dependent liquidity/safety | unresolved | Fixed-window/residual diagnostics describe variation | No measured stress mechanism or prospective regime test |
| M01 | Invalid/carried quote/missing calendar | unresolved | T02/T04/T12 coverage and missingness audits; T14 support diagnosis | External calendar/clock completeness remains scoped; T16 synchronized gaps |
| M02 | Mapping/splits/units | supported | Verified mapping/arithmetic foundation for original samples; T14 ratio-support check | Historical venue/unit completeness still scoped; T16 transition gates held |
| M03 | Equal-cash ex-dividend arithmetic | supported | Documented ratio arithmetic foundation, not a causal payout test | Full cash-inclusive historical panel not certified |
| M04 | Asynchronous class price discovery | unresolved | T05 preferred catch-up; T08 TSMC both-venue adjustment | Descriptive price-leg evidence; causality/executable clocks unresolved |
| M05 | Auction/tick/execution pressure | untested | T14/T16 identify measurement needs, not the mechanism | Not run; actual synchronized auction/quote records missing |
| M06 | Preferred contractual rights | supported | Documented foundation contradicts a blanket US senior-preferred analogy | Historical completeness scoped; rights evidence is not a causal estimate |
| B01 | Persistence/no predictable change | supported | T02 primary benchmark strong; T10/T12–T15 retain real scoped wins elsewhere | Historical Samsung scope; does not assert zero long-run predictability |
| B02 | Global/rolling equilibrium adjustment | contradicted | Archived Samsung contradiction scoped; T12–T15 heterogeneous evidence; T20 matching anchors beat Novo level/state, limited activity exception | Preserve historic scope; future anchor stability and measurement interpretation unresolved |
| B03 | Local short-horizon reversal | unresolved | T01/T03/T05 correction association and exploratory D1 secondary gain | No reliable primary future predictor or executable reversal established |
| B04 | State-dependent nonlinear adjustment | unresolved | T02 history/volatility and T14–T15 support/mean checks do not identify nonlinear economic regimes | General mechanism not established; no further same-data grid authorized |

## 8. What the combined evidence permits

We can retain genuine historical prediction improvements without calling them economic mechanisms or deployable trades. Samsung's limited forecast transfer, heterogeneous US pairs, VW's large losses, and Novo's terminal-anchor result all constrain a universal convergence story. Failed proxy designs constrain those designs; unmeasured ownership, governance, borrow, payout and liquidity branches remain open rather than falsely rejected.

The next information comes from independently qualified measurement and genuinely new origins: validate Novo's source-native FX/auction/receipt clocks and basis, retain every missing slot and interval hold, and evaluate the registered anchor/persistence contrast only after qualified forecasts are actually issued. T20/T21 are a separately user-authorized finite regression batch, not an adaptive model grid. Its historical activity exception does not automatically change the prospective roster. No canonical causal verdict or earlier result was overwritten.

## Evidence and reproducibility note

The narrative and tables synthesize the linked reports, canonical tree, [execution ledger](LONG_HORIZON_EXECUTION_LEDGER.json), [append-only evidence ledger](LOOP_RESEARCH_EVIDENCE_LEDGER.json), public scorecards and the [analyst's original 63-table inventory](LOOP_ANALYST_REVIEW_INVENTORY_20261112.csv), plus subsequently completed LH5, bounded audits and T20/T21. Original artifacts retain detailed uncertainties, failed/blocked fits, source hashes and verification histories. An arithmetic reconstruction is not another economic sample. The productive batch has frozen code/config, source hashes and independent verification. New evidence is appended separately while every canonical historical status and prior source/result is preserved. Licensed observation rows remain private.
