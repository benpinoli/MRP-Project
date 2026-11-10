# LOOP-exception tests: hypotheses, regressions, outcomes, and answers

Run date: November 9, 2026  
Final Slurm job: `15208094`  
Executable output: `runs/loop_exceptions/15208094/results`  
Configuration: `configs/loop_exception_tests.v1.json`

Universe source hashes: workbook DOCX `771ce987aa3e134802c0628c0d85b563746e88b2aeb595e6ae903ffcd62ffc4f`; companies XLSX `bd9e19804811a0cd29e62a88a98de7661833bf193a2344a6349b89790399b331`.

## Executive answer

The broader LOOP workbook changes the Samsung-only conclusion in a useful way. Relative-price correction is not unique to Samsung: five of seven locally available US share-class/preferred pairs have a negative full-sample B00 coefficient at conventional significance levels. But statistical mean reversion is not the same as useful forecasting. In expanding walk-forward tests, every B00 model beats a mechanically aggressive rolling-median forecast, while only Berkshire A/B and Liberty Broadband A/C beat the harder zero-change persistence benchmark. The Liberty gain is very small. A common global factor is weak: the first principal component explains 16.22% of complete-case US differential changes, and exact-calendar correlations with Samsung, SK Square, and TSMC are generally small.

Holdco pass-through is strong for several relationships but incomplete and heterogeneous. Naspers/Prosus is closest to one-for-one; Liberty/Charter, BN/BAM, SoftBank/Arm, and Prosus/Tencent have substantial but sub-unit betas; Investor AB/Atlas is much weaker. Only Liberty/Charter and SoftBank/Arm show conventional evidence of a different downside beta. These are proxy-listing return associations, not NAV discounts.

## H1 — Does short-run relative-price correction generalize?

Regression: `100Δlog(P_left/(units × P_right)) = α + ρ·100log(P_left,t−1/(units × P_right,t−1)) + ε`, with HAC(20). Berkshire uses 1,500 B shares per A share and starts after the January 2010 B-share split.

| Pair | Actual regression sample | n | ρ | HAC(20) SE | p | Adjusted R² | Outcome |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| Alphabet A/C | 2014-03-28–2026-11-06 | 2,988 | −0.00138 | 0.00183 | 0.452 | 0.01% | No conventional evidence |
| Berkshire A/B | 2010-01-22–2026-11-06 | 4,043 | −0.19574 | 0.04020 | 1.12×10⁻⁶ | 9.77% | Correction supported |
| News B/A | 2013-06-20–2026-11-06 | 3,184 | −0.00497 | 0.00198 | 0.0120 | 0.20% | Correction supported; tiny fit |
| Fox B/A | 2019-03-15–2026-11-06 | 1,741 | −0.00443 | 0.00183 | 0.0158 | 0.15% | Correction supported; tiny fit |
| Liberty Broadband A/C | 2014-11-05–2026-08-20 | 2,779 | −0.02809 | 0.00455 | 6.47×10⁻¹⁰ | 1.35% | Correction supported |
| Petrobras common/preferred ADR | 2001-02-22–2026-11-06 | 6,257 | −0.00603 | 0.00164 | 0.00023 | 0.28% | Correction supported; tiny fit |
| Volkswagen common/preferred ADR proxy | 2003-07-08–2026-11-06 | 5,679 | −0.00265 | 0.00224 | 0.237 | 0.11% | No conventional evidence |

Answer: correction generalizes statistically, but explanatory power is usually very low. Berkshire is the clear exception because the two classes have a tight declared economic conversion relationship. Zero is not asserted as fair value for pairs with different voting, dividend, depositary, tax, or liquidity rights.

## H2 — Does an expanding model beat the rolling median and persistence?

The expanding B00 forecast uses only prior observations after a 252-observation minimum. It is compared with zero expected change and with a forecast that moves the next level to its prior 252-session median.

| Pair | Forecast n | B00 RMSE | Persistence RMSE | Rolling-median RMSE | B00 vs persistence | B00 vs median |
| --- | ---: | ---: | ---: | ---: | --- | --- |
| Alphabet | 2,736 | 0.1893 | 0.1892 | 0.8309 | Loses | Wins |
| Berkshire | 3,791 | 0.2600 | 0.2692 | 0.3705 | Wins | Wins |
| News | 2,932 | 0.4332 | 0.4330 | 2.6464 | Loses | Wins |
| Fox | 1,489 | 0.3293 | 0.3278 | 1.8427 | Loses | Wins |
| Liberty Broadband | 2,527 | 0.2626 | 0.2631 | 0.9656 | Wins narrowly | Wins |
| Petrobras | 6,005 | 0.7600 | 0.7599 | 4.9101 | Loses | Wins |
| Volkswagen proxy | 5,427 | 2.7546 | 2.6625 | 28.9143 | Loses | Wins |

Answer: yes, all seven beat the rolling-median forecast, but that benchmark is too aggressive for a next-session level prediction. Only Berkshire improves materially on persistence (about 3.4% RMSE); Liberty improves by about 0.2%. The other five fail the more credible benchmark.

## H3 — Which leg corrects after a widening?

After a one-percentage-point left-relative widening, the average subsequent relative change is negative at 1, 5, and 20 sessions for every pair. The one-session correction ranges from −0.16 points for News to −0.92 points for Berkshire. In the larger event samples, the right leg generally outperforms the left leg after the widening: Petrobras has 452 one-session events and corrects −0.26 points; Volkswagen has 929 and corrects −0.39 points. Berkshire has 21 post-split events and corrects −0.92 points.

Answer: the broad descriptive pattern is catch-up by the relatively cheaper/right security rather than continued divergence. It is not a causal result, and Alphabet (2 events), Liberty (9), and Fox (10) are too sparse for a stable event conclusion.

## H4 — Are quoted spreads and turnover mismatch a common mechanism?

Regression: absolute deviation from the prior 252-session median on standardized combined relative quoted spread and standardized absolute log turnover-proxy difference, with HAC(20).

- Wider combined spreads align with larger deviations for Alphabet (p=0.039), Berkshire (p<10⁻⁸), and Petrobras (p<10⁻¹⁴).
- News has the opposite spread sign (p<10⁻⁸), while Fox and Liberty are not conventionally significant.
- Turnover mismatch signs are also mixed. Volkswagen has no quoted-spread history and is blocked.
- Adjusted R² is 10.7% for Berkshire, 9.5% for News, 32.8% for Petrobras, and below 2.6% for the other estimable pairs.

Answer: transaction-cost/liquidity state matters for some pairs, but there is no universal sign or single liquidity mechanism across the workbook universe. Quotes are also absent for OTC proxies, so a null proxy result cannot reject the broader mechanism.

## H5 — Is a simple z-score trade economically promising?

The diagnostic position opposes a prior-information 252-session z-score when `|z| ≥ 1`, applies the position to the next price-ratio change, and charges half the observed combined relative spread when the position changes. Six pairs with quotes have positive quoted-spread-net annualized log returns, but net Sharpes range from 0.27 to 1.58. Petrobras retains a roughly −41% diagnostic drawdown. Volkswagen has no quoted-spread result and its gross proxy has an unusable −238% cumulative-log drawdown statistic.

Answer: this screen identifies candidates for a real implementation study, especially Berkshire, but it does not answer whether the trade is executable. Borrow availability/fees, dividends, taxes, locate constraints, depositary/conversion costs, market impact, and delisting/merger handling are absent. These figures are not portfolio-performance claims.

## H6 — How strongly do holdcos pass through held-company returns?

Regression: contemporaneous holdco proxy return on heldco proxy return plus an interaction for negative heldco returns, with HAC(20).

| Relationship | Actual sample | n | Up beta | Down beta | Asymmetry p | Adjusted R² | Answer |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| Liberty Broadband/Charter | 2014-11-05–2026-08-20 | 2,782 | 0.878 | 0.959 | 0.019 | 79.8% | High pass-through; stronger down beta |
| BN/BAM | 2022-12-12–2026-11-06 | 798 | 0.817 | 0.804 | 0.845 | 65.3% | High, symmetric pass-through |
| SoftBank/Arm proxy | 2023-09-15–2026-11-06 | 608 | 0.401 | 0.630 | 0.00093 | 51.6% | Partial and downside-asymmetric |
| Prosus/Tencent proxy | 2019-10-23–2026-11-06 | 1,588 | 0.794 | 0.856 | 0.285 | 69.9% | High, no clear asymmetry |
| Naspers/Prosus proxy | 2019-10-23–2026-11-06 | 1,588 | 1.006 | 0.999 | 0.879 | 85.1% | Near one-for-one |
| Investor AB/Atlas proxy | 2014-09-08–2026-11-06 | 2,879 | 0.246 | 0.373 | 0.131 | 12.5% | Weak pass-through |

Answer: the held-company exposure is economically important in five cases, but the wide beta/R² range rejects a one-size-fits-all holdco mapping. These regressions cannot measure NAV discounts without dated holdings, other assets, liabilities, taxes, and share counts.

## H7 — Is there a global related-security gap factor?

PCA on 1,662 complete US dates from 2019-03-15 through 2026-08-20 gives only 16.22% variance to PC1. Loadings have mixed signs. Exact-calendar correlations between the seven US pair changes and the three core pairs are mostly near zero; the largest absolute values are TSMC/Berkshire at −0.134 and TSMC/Volkswagen at +0.100. Asian/US close timing is not synchronized.

Answer: no dominant global gap factor appears in this specification. A regional or rights-matched factor remains possible, but the current evidence argues against treating all LOOP exceptions as one trade.

## H8 — Does the Samsung-style factor/gap design transfer to Prosus/Tencent?

The previously staged local-security sensitivity was completed in Slurm job `15208213` under `runs/core_pairs/prosus_tencent_15208213`. The panel has 1,841 common dates from 2019-09-11 through 2026-09-30, 1,734 usable levels, and 1,611 full-model observations after exact FX/factor alignment. It is a normalized contemporaneous USD price ratio, not Prosus NAV.

Full-window HAC(20) adjusted R² is 0.62% for B01, 0.48% for B02, 0.71% for B03, and 0.66% for B04. B03's lagged-gap coefficient is −0.00263 (p=0.0183), but its batch BH q-value is 0.634. In B04 it weakens to −0.00234 (p=0.0713), and lagged relative activity is −0.0285 (p=0.650). No factor coefficient survives BH adjustment; the minimum full-sample q-value is 0.634. The 2005–2014 window is outside coverage and 2015–2019 has only 70 aligned observations, so both are correctly blocked.

Answer: the Samsung-style design transfers operationally, but not as a strong explanatory model. There is nominal weak gap adjustment, negligible fit, no incremental activity evidence, and no multiplicity-robust factor finding. The stronger existing exact-interval return regressions remain the appropriate evidence for Tencent exposure; neither design supplies historical NAV or a trading signal.

## Coverage, identifiers, actions, and missing fields

- The seven share-pair panels contain 1,741–6,257 usable changes after pair-specific structural starts. All selected listings are USD and BARRID/date keys are unique.
- Effective identifier histories are preserved in `identity_missing_audit.csv`; several BARRIDs span ticker/name changes. The analysis keys on BARRID, not the current ticker string.
- The naive action patch masks 0–27 boundaries per pair where vendor and price-implied returns differ by more than three percentage points. It changes no raw price and performs no interpolation.
- Quote history is incomplete for early Alphabet, Berkshire, and Petrobras observations and entirely absent for several OTC proxies. Volkswagen quote-based tests are blocked.
- Licensed Parquets are read in place and never copied into tracked output. The run manifest records source paths, sizes, modification times, configuration hash, and all aggregate output hashes.

## Core-pair continuation verification

The disconnect-era run at `runs/core_pairs/baseline_20261109` was independently regenerated during this batch. All 17 raw-file SHA-256 values matched the original manifest before and after the rerun. Coverage, identifier, fundamentals, and manifest outputs matched exactly; floating results matched within 4.1×10⁻¹⁶ under the alternate project environment. The notebook contains one core-pair checkpoint and one matching code table. The completed results remain in `CORE_PAIR_BASELINE_RESULTS.md`.

The Korean NAV regressions remain pending. Commit `3666efa`, the Korean filings, and the ownership CSV provide individual observations, not dated ownership histories. Original executable WRDS queries are still missing for Global daily, annual fundamentals, both CRSP daily exports, CRSP name history, and Global descriptors; FRED retrieval/vintage metadata are also absent.

## Exact workbook tests still blocked

Exact local tests still require additional primary/local exports or structural histories for Alibaba, HDFC, Shell, Novo Nordisk, BYD, Ping An, Hyundai, Exor/Ferrari, Industrivarden/Volvo, Roche, and the German Volkswagen classes. US proxy listings are not silently substituted for exact primary/ADR, A/H, local-class, or NAV tests.
