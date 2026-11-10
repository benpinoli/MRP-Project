# Hypothesis-resolution results — November 9, 2026

Empirical run: `runs/hypothesis_resolution/15204916/results`  
Slurm job: `15204916` (`COMPLETED`, 28 seconds, peak RSS 123 MB)  
Configuration: `configs/hypothesis_resolution_v1.json`

## Executive findings

Four currently answerable questions were tested.

1. **Relative non-treasury share supply describes Samsung discount regimes but does not explain annual changes or the large movement during the stable-count era.** The simple supply-only explanation is insufficient.
2. **After a Samsung discount widening, subsequent relative correction comes primarily through preferred-share catch-up.** Common-price reversal contributes at five sessions but is not stable at one or twenty sessions.
3. **The recent Samsung repurchase programs were almost class-proportional, and their event paths were mixed.** They do not provide clean evidence that preferred-relative issuer support caused discount narrowing.
4. **TSMC parity correction occurs in both markets.** An ADR-over-local gap at the Taiwan close predicts a later ADR decline, while a gap at the US close predicts a next-session Taiwan-local increase. This survives an ADR-spread sensitivity.

None of these results is a causal estimate, point-in-time forecast validation, fair-value model, or executable trading test.
The horizons, outcomes, clocks, and sensitivities were fixed before the final run. Reported p-values are exploratory and are not multiplicity-adjusted; related horizons and class-return outcomes are mechanically dependent.

## H1 — Samsung supply versus trading capacity

### Hypothesis

Persistent Samsung discount changes are related to the preferred/common non-treasury share ratio, relative trading activity, or both. Scarcity support and impaired trading capacity are competing mechanisms.

### Regression

The annual panel has 17 joint level observations (2005 and 2010–2025) and 15 consecutive first differences (2011–2025). Models use HC1 OLS. The joint level regression includes relative supply, relative activity, and a linear time control. Partial permutation p-values use 20,000 fixed-seed permutations. Rank correlations provide a specification-light check.

| Specification | Variable | Coefficient | HC1 SE | Partial permutation p | n | R² |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| Levels, univariate | P/C non-treasury ratio | 1046.75 | 197.92 | 0.00015 | 17 | 0.6984 |
| Levels, univariate | P/C relative activity | −10.99 | 7.15 | 0.2603 | 17 | 0.0828 |
| Levels, joint + time | P/C non-treasury ratio | 912.11 | 587.78 | 0.0921 | 17 | 0.7025 |
| Levels, joint + time | P/C relative activity | −2.87 | 6.40 | 0.6517 | 17 | 0.7025 |
| First differences, joint | Change in P/C non-treasury ratio | −11.46 | 551.12 | 0.9864 | 15 | 0.0006 |
| First differences, joint | Change in P/C relative activity | 0.70 | 7.71 | 0.9316 | 15 | 0.0006 |

The level Spearman correlation between discount and relative non-treasury supply is 0.790 (p=0.00016). The corresponding first-difference rank correlation is −0.036 (p=0.898). Relative activity is weak in levels and changes.

### Outcome

The level relationship is real descriptively but is not a change relationship and weakens materially once activity and time are included. Most decisively, the preferred/common non-treasury ratio is effectively constant from 2018–2023, while the annual discount ranges from 8.92 to 18.53 percentage points—a 9.61-point range.

### Question answered

**Can relative non-treasury supply alone explain persistent Samsung discount movements? No.** It can mark long-run regimes, but it cannot explain substantial variation while the measured count ratio is unchanged. The relative-activity proxy also does not explain annual changes. True spreads, depth, public float, and ownership remain unmeasured, so the broader liquidity and investor-base mechanisms remain unresolved.

## H2 — Which Samsung share class adjusts after a widening?

### Hypothesis

If a widening is transient, preferred shares should subsequently outperform common shares. If correction instead comes from common-price reversal, the common forward-return coefficient should be negative.

### Regression

Adjusted common, preferred, and preferred-minus-common forward log returns at 1, 5, and 20 observed sessions are regressed on the current discount change. Flagged or missing-price intervals are excluded without bridging. Newey–West lag is `max(5, horizon)`. Coefficients below are responses per one percentage-point widening.

| Horizon | Common return | Preferred return | Preferred − common | Relative p-value | Relative adjusted R² |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 1 session | −0.000169 (p=0.619) | 0.001272 (p=0.00037) | 0.001442 | 1.54×10⁻¹¹ | 0.0110 |
| 5 sessions | −0.001834 (p=0.0185) | 0.002005 (p=0.0073) | 0.003839 | 7.29×10⁻²⁸ | 0.0222 |
| 20 sessions | −0.001396 (p=0.172) | 0.003920 (p=0.000023) | 0.005316 | 2.00×10⁻³⁹ | 0.0175 |

The positive relative coefficient appears in each fixed calendar subperiod. Explanatory power remains low.

### Outcome

A one-point widening is followed by approximately 0.14%, 0.38%, and 0.53% preferred-over-common log-return correction over 1, 5, and 20 sessions. Preferred catch-up is positive at all three horizons. Common reversal is distinguishable from zero only at five sessions in the full sample.

### Question answered

**Which leg produces the observed short-horizon adjustment? Primarily the preferred share.** This supports preferred catch-up as the descriptive channel. It does not prove stale prices, investor identity, executable reversal, or out-of-sample forecast value; bid–ask bounce and auction effects remain rivals.

## H3 — Recent repurchase, cancellation, and dividend disclosures

### Hypothesis

Preferred-relative issuer support should narrow the discount after information becomes observable. A cancellation of already-held treasury shares must not be treated as a second market purchase.

### Design

The predeclared issuer batch reports 1-, 5-, and 20-session discount changes from the conservative next observed proxy session. Six disclosures represent only three connected clusters. Publication clocks are unknown, so this is a descriptive case study rather than an iid event regression.

### Outcome

| Disclosure | Relative dose or information | 1-session Δq | 5-session Δq | 20-session Δq |
| --- | --- | ---: | ---: | ---: |
| 2024 authorization | Essentially equal fractions: P−C ≈ 0.00000008 pp issued | +0.45 | +1.35 | +2.34 |
| 2024 execution report | Same connected program and near-equal fractions | −2.08 | −1.06 | −1.00 |
| Cancellation decision | Previously repurchased shares; not new demand | −0.69 | +1.38 | +1.10 |
| 2025 authorization | P−C = −0.00086 pp issued | +0.33 | +0.30 | +1.20 |
| 2025 execution report | P−C = +0.01383 pp issued | +0.25 | +2.20 | +1.90 |
| FY2024 dividend decision | Common KRW363, preferred KRW364 | −0.20 | +0.22 | −0.61 |

Positive Δq means widening. The execution-report dates are not the historical purchase dates; reported aggregates were not spread backward across the execution window.

### Question answered

**Do these recent programs identify preferred-relative buyback support as the cause of narrowing? No.** The programs were nearly class-proportional, and observed paths are mixed. The 2024 execution report precedes narrowing, but the 2024 authorization and both 2025 program disclosures precede widening over the reported windows. Connected stages, anticipation, endogenous program timing, and unknown clocks prevent a causal interpretation.

## H4 — TSMC cross-market price discovery

### Hypothesis

If the ADR is expensive relative to five Taiwan shares at the Taiwan close, the later US ADR should fall. If the ADR remains expensive at the US close, the next Taiwan-local close should rise. These signs reveal which venue participates in parity correction.

### Regression

The Taiwan-close state uses the previous ADR close and latest FX fixing strictly before the Taiwan date. Its outcome is the later same-calendar-date ADR price return. The US-close state uses the same-date Taiwan close and noon-New-York FX; its outcome is the next Taiwan-session local return. Regressions use HAC(5). A sensitivity removes ADR relative spreads above the historical 90th percentile (0.001101).

| Clock | Coefficient | HAC SE | p-value | n | Adjusted R² |
| --- | ---: | ---: | ---: | ---: | ---: |
| Taiwan close → later US close | −0.04510 | 0.00616 | 2.50×10⁻¹³ | 5,407 | 0.0152 |
| US close → next Taiwan close | +0.06116 | 0.00454 | 2.63×10⁻⁴¹ | 5,359 | 0.0445 |
| Taiwan → US, spread sensitivity | −0.03947 | 0.00607 | 7.91×10⁻¹¹ | 4,887 | 0.0127 |
| US → Taiwan, spread sensitivity | +0.05869 | 0.00463 | 7.69×10⁻³⁷ | 4,841 | 0.0439 |

The signs persist in 2005–2014, 2015–2019, and 2020–2026. Adjustment was much stronger in 2015–2019: −0.371 from Taiwan to the US and +0.390 from the US to Taiwan.

### Outcome

Both venues participate. A 1% log parity gap at the Taiwan close predicts about a 0.045% later ADR move toward parity. A 1% gap at the US close predicts about a 0.061% next-session Taiwan-local move toward parity. The next-Taiwan regression has greater explanatory power in the full sample.

### Question answered

**Where does TSMC parity correction occur? In both markets, with a somewhat stronger measured next-Taiwan component.** This materially narrows the timing explanation for the earlier B00 result. It does not establish executable arbitrage because local bid/ask quotes, conversion fees, creation/cancellation constraints, borrow, and simultaneous executable prices remain unavailable.

## Remaining unresolved questions

- Korean NAV and ownership mechanisms require dated ownership histories and point-in-time valuation inputs.
- Samsung payout delivery requires a reviewed DPS/policy/publication-date panel from the locally acquired annual reports.
- Borrow fees, lendable inventory, historical KRX short positions, Samsung GDR parity, and true Korean bid/ask/depth remain unavailable.
- The Samsung catch-up result needs an untouched future cohort and executable-price validation before it can become a forecasting or trading claim.

## Reproducibility

The successful run produced:

- `annual_supply_regressions.csv` and `annual_rank_diagnostics.csv`
- `samsung_leg_adjustment.csv` and its analysis panel
- `issuer_event_windows.csv` and `issuer_event_doses.csv`
- `tsmc_price_discovery.csv` and its clock-aligned panel
- `manifest.json` with input, configuration, and code hashes

Run with `slurm/hypothesis_resolution.sbatch`. Four synthetic/unit checks passed inside the allocation. The earlier job `15204801` failed before estimation because three missing preferred-price days triggered an overly strict assertion; the final code leaves those endpoints missing and prevents bridging. Job `15204863` completed but omitted the valid 2010→2011 annual difference; final job `15204916` corrected the sample to all 15 consecutive changes.
