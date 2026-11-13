# Complete five-snapshot receipt and analyst diagnostics

November 12, 2026. All five acquisition snapshots are installed and verified in
the authorized private repository. Existing qualified price work continued with
diagnostics of saved forecasts, without new fits or sample extensions. A separate
analyst reviewed 63 aggregate tables across 16 completed research families against
the hypothesis tree and original literature. Prior estimates and verdicts remain
unchanged. No executable trading opportunity is certified.

## Receipt and installation

Main was fetched and fast-forwarded to `3860c39`, preserving all uncommitted
v2/v3 work and the winners document. Main matches origin/main; current work is
on `data/loop-long-horizon-v4-20261112`. AGENTS.md, the current ORC instructions,
and applicable development/storage/security/Slurm/Python/software/performance
guidance were read. Sustained I/O and computation used Slurm.

The complete transfer is
`data/acquisition/2026-11-12_v1/wrds_complete_transfer_2026-11-12_v1.zip`:
**942,656,553 bytes**, SHA-256
`709b31f15d7935f651a37d8603143d949300f48abcf76381aa5c660d95396dc0`.
Receipt job `15308639` verified the trusted size/hash and all 66 outer entries,
including entry sizes/hashes/CRCs, exact inventory and path/type/symlink checks.
It staged the package at `data/acquisition/complete_transfer_v4_15308639/`
without flattening paths.

README.md, FINAL_AGENT_PROMPT.md, BUNDLE_INDEX.json, TRANSFER_INVENTORY.json and
the standard-library installer were reviewed. Job `15308656` ran both requested
commands from staging:

```bash
python verify_install.py
python verify_install.py --repo-root /home/bpinoli/MRP/MRP-Project
```

Both commands passed. The installer preflighted all target files, retained
identical existing files and installed the fifth snapshot without overwriting
differing local work. The authoritative ZIPs and delivery JSONs remain in staged
`bundles/`; installed directories retain original project-relative paths.

| Installed snapshot | Target directory under data/acquisition/ | Verified entries |
| --- | --- | ---: |
| Descriptors | `2026-11-11/wrds_descriptor_review/` | 95 |
| Daily prices/mapping | `2026-11-12/wrds_daily_and_mapping/` | 46 |
| Long-history follow-up | `2026-11-12/loop_long_horizon_followup/` | 273 |
| Gap-closure supplement | `2026-11-12/loop_gap_closure_supplement/` | 138 |
| Public-report additions | `2026-11-12/loop_public_report_additions/` | 48 |

All 600 installed delivery entries were independently rehashed at point of use;
176 reused/prerequisite reference records resolve with matching source hashes.
These include repeated references, not 176 distinct documents. Read each snapshot's
original notes/handoff where present, coverage, source inventories, validation
and applicable revision alerts. Convenience notes were not substituted for the
authoritative installed snapshots. No licensed content was added to Git.

## New evidence admission

The fifth snapshot adds 616 facts (VW 257, Novo 201, Hyundai 158),59 cited sources,
four separate Novo report-availability bounds,47 passing extraction checks and
eight revision/source alerts. Its59 previously delivered exact transcriptions
remain excluded; different report vintages remain distinct evidence.

The v4 private registry preserves all 1,991 selected facts across the three newer
evidence snapshots. **1,981 have unknown first-publication dates.** Ten dated facts
remain evidence only; this diagnostic specification admits **zero new structural
forecast features**. Four report-availability clocks are retained separately,
including their explicit “unknown; availability confirmed by this announcement”
qualification. Their bounds do not prove earliest dissemination or identical
first-publication PDF bytes, and do not overwrite annual unknowns or backdate
comparative observations.

Retained alerts include VW's initial2019 dividend proposal and subsequent
reduction; residual other-shareholder versus free-float definitions; Novo's
2014/2023 split-restated nominal units; Hyundai's2009/2010 interior-header
discrepancy,2021 split year token and separate interim/final/proposed components.
Missing values are not zeros, dividend-eligible counts are not year-end supply,
and aggregate holdings are not allocated to classes. All prior vendor/issuer
share-basis exceptions, local/US split clocks and distribution rows survive.

## Existing sample coverage

**No backward paired interval was admitted.** Current exchange attributes and
listing anchors still do not certify historical quote-source venue. Pre-Xetra
VW stays excluded; Novo predecessor/demerger/Nasdaq periods stay separate;
Hyundai third preferred has no positive pre-2005 price; HDFC's first-price versus
metadata-start discrepancy remains. Unit/currency, dated-ID, status, corporate
transition and ratio gates still apply independently of archive integrity.

The frozen original monthly panels contain14 class samples. Eleven have eligible
two/five-year forecasts; Alibaba, unified Shell and Roche participation remain
too short. The table shows pragmatic coverage-qualified months under the original
measurement assumptions, **not new historical exact-venue certification**.
Strict coverage and level-model forecast-origin counts are in the
[coverage table](LOOP_LONG_HORIZON_V4_COVERAGE_20261112.csv).

| Existing comparison | Qualified monthly span | Pragmatic months | 24 m / 60 m level origins |
| --- | --- | ---: | ---: |
| Alibaba local/ADS | 2019-12–2026-09 | 82 | 0 / 0 |
| BYD A/H | 2011-07–2026-10 | 182 | 99 / 27 |
| HDFC local/ADS | 2005-01–2026-09 | 261 | 178 / 106 |
| Hyundai common/preferred 1 | 2005-01–2026-10 | 259 | 173 / 107 |
| Hyundai common/preferred 2 | 2005-01–2026-10 | 259 | 173 / 107 |
| Hyundai common/preferred 3 | 2006-05–2026-10 | 246 | 163 / 91 |
| Novo local/ADS | 2005-01–2026-09 | 260 | 176 / 105 |
| Ping An A/H | 2007-03–2026-10 | 234 | 151 / 81 |
| Roche voting/Genussschein | 2005-01–2026-03 | 255 | 172 / 100 |
| Roche voting/participation | 2026-03–2026-10 | 8 | 0 / 0 |
| Historical Shell A | 2005-08–2022-01 | 198 | 115 / 43 |
| Historical Shell B | 2005-08–2022-01 | 198 | 115 / 43 |
| Unified Shell | 2022-02–2026-09 | 56 | 0 / 0 |
| VW ordinary/preferred | 2005-01–2026-10 | 262 | 179 / 107 |

Missing months remain missing and the calendar grid is retained. There is no
ten-year evaluation. The eight strict Ping An five-year activity origins blocked
by the v3 rolling training minimum stay blocked; the level counts above do not
hide those model-specific failures. Shell and Roche transitions remain separate.
Unsynchronized closes, reference FX and matched-ratio/quote-scale assumptions
retain their original limitations; no provider return series was spliced.

## Price and unit diagnostics

[V4 protocol](LOOP_LONG_HORIZON_V4_PROTOCOL_20261112.md) and
`configs/loop_long_horizon_v4.json` freeze these diagnostics. Private run:
`runs/loop_long_horizon/v4_15308800/`. All 524 v3 method/window/model/horizon/coverage
score rows and 54,748 saved forecast-variant cases were retained. There are no new
predictive fits, penalty/window selection, favorable-origin exclusions or
prospective outcomes. Counts across variants are dependent.

Public aggregates: [forecast diagnostics](LOOP_LONG_HORIZON_V4_DIAGNOSTICS_20261112.csv)
and [drawdown-units review](LOOP_LONG_HORIZON_V4_DRAWDOWN_UNITS_20261112.csv).

**Impossible forecast support.** There are 316 forecast-variant cases with predicted
terminal discount at or above100%. Every actual panel uses
`q=100*(1-positive price ratio)`, so q<100. A forecast q>=100 implies a nonpositive
price-ratio equivalent. All 316 are unconstrained OLS forecasts: VW at 24 months,
Hyundai preferred 3 at 24/60 months and preferred 2 at 60 months. These are model
support failures, not observed negative prices, independent episodes or trading
opportunities. No saved ridge prediction breaches this bound, but that is a
diagnostic comparison rather than a post-hoc selection of ridge for deployment.
No forecast was clipped or removed.

**Weak-benchmark wins.** In161 of 524 score rows, the model beats its training-mean
benchmark while failing to beat persistence. VW's pragmatic five-year level OLS
has R-squared−0.0759 against persistence but+0.8692 against the expanding mean;
that mean's MSE is 8.226 times persistence MSE. Under rolling training the mean
benchmark is 7.636 times persistence MSE. Both comparisons are retained. Beating
an unstable mean does not establish strong prediction.

**Extrapolation and concentration.** VW's pragmatic two-year level OLS has32
discount-state extrapolation origins under expanding training and 57 under rolling
training. Its largest squared-loss origin-year cohort is 2011, accounting for
40.8%/39.8% of total loss, respectively. This does not identify the 2008 squeeze
as the sole cause. Source/support and training-regime rivals remain open. Novo's
pragmatic level model has only1 expanding/4 rolling two-year extrapolation origins
and none at five years. Its largest loss cohorts are 2024 at two years and 2021 at
five years, roughly22–25% and 28–33% of total loss. Calendar cohorts overlap in
their economic outcomes and cannot be treated as independent episodes.

**Drawdown dimensions.** The earlier US LOOP output's VW gross value−238.1755
is 100 times a cumulative log-score drawdown, not a proportional wealth loss.
The same-peak geometric-index translation is **−90.7612%**. The new table retains
the original values and translates all 14 pair/scope rows, preserving VW's
unavailable quoted-net value as missing. It does not reconstruct the omitted
initial zero peak, a funded long/short wealth account, next executable fills,
borrow/funding, dividends, taxes or impact. The conversion does not make the
strategy executable or economically attractive. Historical outputs are unchanged.

## Independent verification and execution record

Verification job `15308863` passed all 524 score diagnostics,54,748 origin
diagnostics,14 unit-translation rows and 1,991 preserved evidence rows, including
the separate availability bounds and revision alerts. Prior inputs and baseline,
v2/v3 outputs remain hash-identical. Private verification:
`runs/loop_long_horizon/v4_15308800/verification_v2/AUDIT.json`.

The scientific outputs and hashes were completed by `15308800`, but its final
console-only JSON print failed on a NumPy integer. The saved summary/progress
and all diagnostic files were intact; the separate successful verification
audited those exact files without recomputing analyses. The future console
logger is fixed. Earlier `15308757` stopped before price diagnostics on the
annotated unknown-date convention. Initial audit `15308814` passed the forecast
checks then rejected the missing VW net drawdown; the retry explicitly verifies
missing against missing. No missing value was filled or source repaired.
All attempts remain preserved. Synthetic tests cover benchmark comparisons,
discount support, log-index units, annotated unknown dates, missing drawdown
preservation and NumPy-count JSON logging.

## Analyst review and remaining blockers

The separately authorized [analyst report](LOOP_ANALYST_REVIEW_20261112.md) ranks
13 tree-linked findings, with a [63-table inventory](LOOP_ANALYST_REVIEW_INVENTORY_20261112.csv),
primary literature links, access limitations and exact falsification tests.
It covers Samsung baselines/locked/continuations/long horizons, core pairs,
Prosus/Tencent/Naspers, hypothesis-resolution supply/legs/events/TSMC, US LOOP
exceptions and LH1–v4. It is an economic/methodological review, not a new
reproduction of every historical coefficient or licensed row.

| Affected analysis | Remaining blocker / next discriminating work |
| --- | --- |
| Backward LOOP samples, M01/M02 | Dated exact local quote provenance plus identity, units, status, corporate/split/ratio checks; no venue relaxation. |
| Structural predictors, S06/G/P branches | Reconcile class/aggregate, issued/net/treasury, nominal/split bases and definitions; independently qualify first-release/revision timing. |
| Novo cash/cross-market, X01–X03/P03 | Exact ratio/close/FX reconciliation, event-specific cash basis and investor treatment; general fee-effective and holder-notice dates remain unknown. |
| LOOP prediction, B01/B02 | Retain impossible/support/extrapolation and weak-benchmark failures; few independent spans and no untouched prospective validation. |
| Berkshire trading candidate | One-way conversion anchors differ by direction; executable next fills, matched quote dates, borrow/funding/cash costs and a funded account remain unverified. |
| TSMC timing anomaly | Audit quote/FX/split clocks and shared-endpoint noise, especially2015–2019; correction signs alone do not prove profitable discovery. |
| News liquidity-sign tension, L01 | Signed premium and class-relative cost estimands, stale quotes and dated control/access channels; no universal causal sign inferred. |
| Holdco/NAV mechanisms | Dated holdings, liabilities, tax and share counts with publication vintages; price-return betas are exposures, not NAV. |

Berkshire and Novo merit the first implementation/measurement challenges;
neither is presently certified as exploitable. VW and Hyundai's invalid-support
forecasts are negative controls for unconstrained linear prediction. No current
literature has been shown overturned. The review distinguishes different
estimands and heterogeneous rights from genuine contradiction, and retains
prior negative evidence rather than searching for favorable specifications.

All acquisition archives, licensed rows, crosswalks, source facts, monthly panels
and individual forecasts remain in ignored private paths. Public changes are
reusable code, aggregate summaries and source-linked research documentation.
