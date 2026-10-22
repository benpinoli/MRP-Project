# Samsung research log and artifact index

This is the clickable record of experiments and files. Canonical file catalog: [research/artifacts.json](../research/artifacts.json). Append-only [observations](../research/observations.jsonl) and [decisions](../research/decisions.jsonl) preserve prior claims and revisions. Raw and derived licensed artifacts remain local and Git-ignored.

[Hypothesis tree](HYPOTHESES.md) · [Methodology](METHODOLOGY.md) · [Run folders](../runs/README.md)

## Current descriptive packs

### 20261022T070352_803683Z

Review status: superseded for episode gap display. Initial pack numerics are retained. Visual inspection found the local 2017 episode line bridged carried/missing dates. Corrected in methodology 3.0.1 and a fresh run; other main/sensitivity plots were visually checked.

[Run overview](../runs/samsung/EP01_descriptive/20261022T070352_803683Z/README.md) · [episode review](../runs/samsung/EP01_descriptive/20261022T070352_803683Z/episodes/REVIEW.md) · [manifest](../runs/samsung/EP01_descriptive/20261022T070352_803683Z/manifest.json)

| ID | Filename | Main | Sensitivity |
|---|---|---|---|
| EP01_F01 | `01_discount_history.png` / `.svg` | [PNG](../runs/samsung/EP01_descriptive/20261022T070352_803683Z/figures/main/01_discount_history.png) · [SVG](../runs/samsung/EP01_descriptive/20261022T070352_803683Z/figures/main/01_discount_history.svg) | [PNG](../runs/samsung/EP01_descriptive/20261022T070352_803683Z/figures/sensitivity/01_discount_history.png) · [SVG](../runs/samsung/EP01_descriptive/20261022T070352_803683Z/figures/sensitivity/01_discount_history.svg) |
| EP01_F02 | `02_annual_distributions.png` / `.svg` | [PNG](../runs/samsung/EP01_descriptive/20261022T070352_803683Z/figures/main/02_annual_distributions.png) · [SVG](../runs/samsung/EP01_descriptive/20261022T070352_803683Z/figures/main/02_annual_distributions.svg) | [PNG](../runs/samsung/EP01_descriptive/20261022T070352_803683Z/figures/sensitivity/02_annual_distributions.png) · [SVG](../runs/samsung/EP01_descriptive/20261022T070352_803683Z/figures/sensitivity/02_annual_distributions.svg) |
| EP01_F03 | `03_daily_discount_changes.png` / `.svg` | [PNG](../runs/samsung/EP01_descriptive/20261022T070352_803683Z/figures/main/03_daily_discount_changes.png) · [SVG](../runs/samsung/EP01_descriptive/20261022T070352_803683Z/figures/main/03_daily_discount_changes.svg) | [PNG](../runs/samsung/EP01_descriptive/20261022T070352_803683Z/figures/sensitivity/03_daily_discount_changes.png) · [SVG](../runs/samsung/EP01_descriptive/20261022T070352_803683Z/figures/sensitivity/03_daily_discount_changes.svg) |
| EP01_F04 | `04_raw_closes_since_2019.png` / `.svg` | [PNG](../runs/samsung/EP01_descriptive/20261022T070352_803683Z/figures/main/04_raw_closes_since_2019.png) · [SVG](../runs/samsung/EP01_descriptive/20261022T070352_803683Z/figures/main/04_raw_closes_since_2019.svg) | [PNG](../runs/samsung/EP01_descriptive/20261022T070352_803683Z/figures/sensitivity/04_raw_closes_since_2019.png) · [SVG](../runs/samsung/EP01_descriptive/20261022T070352_803683Z/figures/sensitivity/04_raw_closes_since_2019.svg) |
| EP01_F05 | `05_trading_activity.png` / `.svg` | [PNG](../runs/samsung/EP01_descriptive/20261022T070352_803683Z/figures/main/05_trading_activity.png) · [SVG](../runs/samsung/EP01_descriptive/20261022T070352_803683Z/figures/main/05_trading_activity.svg) | [PNG](../runs/samsung/EP01_descriptive/20261022T070352_803683Z/figures/sensitivity/05_trading_activity.png) · [SVG](../runs/samsung/EP01_descriptive/20261022T070352_803683Z/figures/sensitivity/05_trading_activity.svg) |
| EP01_F06 | `06_rolling_discount_volatility.png` / `.svg` | [PNG](../runs/samsung/EP01_descriptive/20261022T070352_803683Z/figures/main/06_rolling_discount_volatility.png) · [SVG](../runs/samsung/EP01_descriptive/20261022T070352_803683Z/figures/main/06_rolling_discount_volatility.svg) | [PNG](../runs/samsung/EP01_descriptive/20261022T070352_803683Z/figures/sensitivity/06_rolling_discount_volatility.png) · [SVG](../runs/samsung/EP01_descriptive/20261022T070352_803683Z/figures/sensitivity/06_rolling_discount_volatility.svg) |
| EP01_F07 | `flagged_discount_windows.png` / `.svg` | [PNG](../runs/samsung/EP01_descriptive/20261022T070352_803683Z/episodes/flagged_discount_windows.png) · [SVG](../runs/samsung/EP01_descriptive/20261022T070352_803683Z/episodes/flagged_discount_windows.svg) | Local inspection |

Exact non-figure files:

- [episodes/flagged_episode_comparison.csv](../runs/samsung/EP01_descriptive/20261022T070352_803683Z/episodes/flagged_episode_comparison.csv)
- [episodes/REVIEW.md](../runs/samsung/EP01_descriptive/20261022T070352_803683Z/episodes/REVIEW.md)
- [episodes/source_rows_around_flags.csv](../runs/samsung/EP01_descriptive/20261022T070352_803683Z/episodes/source_rows_around_flags.csv)
- [provenance/environment.json](../runs/samsung/EP01_descriptive/20261022T070352_803683Z/provenance/environment.json)
- [provenance/METHODOLOGY.md](../runs/samsung/EP01_descriptive/20261022T070352_803683Z/provenance/METHODOLOGY.md)
- [provenance/source_inventory.json](../runs/samsung/EP01_descriptive/20261022T070352_803683Z/provenance/source_inventory.json)
- [provenance/validation.txt](../runs/samsung/EP01_descriptive/20261022T070352_803683Z/provenance/validation.txt)
- [provenance/worktree.patch](../runs/samsung/EP01_descriptive/20261022T070352_803683Z/provenance/worktree.patch)
- [README.md](../runs/samsung/EP01_descriptive/20261022T070352_803683Z/README.md)
- [tables/annual_distributions.csv](../runs/samsung/EP01_descriptive/20261022T070352_803683Z/tables/annual_distributions.csv)
- [tables/field_coverage.csv](../runs/samsung/EP01_descriptive/20261022T070352_803683Z/tables/field_coverage.csv)
- [tables/flagged_dates.csv](../runs/samsung/EP01_descriptive/20261022T070352_803683Z/tables/flagged_dates.csv)
- [tables/issue_inventory.csv](../runs/samsung/EP01_descriptive/20261022T070352_803683Z/tables/issue_inventory.csv)
- [tables/largest_changes.csv](../runs/samsung/EP01_descriptive/20261022T070352_803683Z/tables/largest_changes.csv)
- [tables/measures_main.csv](../runs/samsung/EP01_descriptive/20261022T070352_803683Z/tables/measures_main.csv)
- [tables/measures_sensitivity.csv](../runs/samsung/EP01_descriptive/20261022T070352_803683Z/tables/measures_sensitivity.csv)
- [tables/raw_quality.json](../runs/samsung/EP01_descriptive/20261022T070352_803683Z/tables/raw_quality.json)
- [tables/summary.json](../runs/samsung/EP01_descriptive/20261022T070352_803683Z/tables/summary.json)

Every snapshot/support file and hash is retained in the manifest and artifact catalog.

### 20261022T070701_403388Z

Review status: verified. All six main/sensitivity layouts inspected; corrected episode plot inspected. Independent saved-output arithmetic and local links verified; raw unchanged. Remaining quote/calendar flags are not resolved.

[Run overview](../runs/samsung/EP01_descriptive/20261022T070701_403388Z/README.md) · [episode review](../runs/samsung/EP01_descriptive/20261022T070701_403388Z/episodes/REVIEW.md) · [manifest](../runs/samsung/EP01_descriptive/20261022T070701_403388Z/manifest.json)

| ID | Filename | Main | Sensitivity |
|---|---|---|---|
| EP01_F01 | `01_discount_history.png` / `.svg` | [PNG](../runs/samsung/EP01_descriptive/20261022T070701_403388Z/figures/main/01_discount_history.png) · [SVG](../runs/samsung/EP01_descriptive/20261022T070701_403388Z/figures/main/01_discount_history.svg) | [PNG](../runs/samsung/EP01_descriptive/20261022T070701_403388Z/figures/sensitivity/01_discount_history.png) · [SVG](../runs/samsung/EP01_descriptive/20261022T070701_403388Z/figures/sensitivity/01_discount_history.svg) |
| EP01_F02 | `02_annual_distributions.png` / `.svg` | [PNG](../runs/samsung/EP01_descriptive/20261022T070701_403388Z/figures/main/02_annual_distributions.png) · [SVG](../runs/samsung/EP01_descriptive/20261022T070701_403388Z/figures/main/02_annual_distributions.svg) | [PNG](../runs/samsung/EP01_descriptive/20261022T070701_403388Z/figures/sensitivity/02_annual_distributions.png) · [SVG](../runs/samsung/EP01_descriptive/20261022T070701_403388Z/figures/sensitivity/02_annual_distributions.svg) |
| EP01_F03 | `03_daily_discount_changes.png` / `.svg` | [PNG](../runs/samsung/EP01_descriptive/20261022T070701_403388Z/figures/main/03_daily_discount_changes.png) · [SVG](../runs/samsung/EP01_descriptive/20261022T070701_403388Z/figures/main/03_daily_discount_changes.svg) | [PNG](../runs/samsung/EP01_descriptive/20261022T070701_403388Z/figures/sensitivity/03_daily_discount_changes.png) · [SVG](../runs/samsung/EP01_descriptive/20261022T070701_403388Z/figures/sensitivity/03_daily_discount_changes.svg) |
| EP01_F04 | `04_raw_closes_since_2019.png` / `.svg` | [PNG](../runs/samsung/EP01_descriptive/20261022T070701_403388Z/figures/main/04_raw_closes_since_2019.png) · [SVG](../runs/samsung/EP01_descriptive/20261022T070701_403388Z/figures/main/04_raw_closes_since_2019.svg) | [PNG](../runs/samsung/EP01_descriptive/20261022T070701_403388Z/figures/sensitivity/04_raw_closes_since_2019.png) · [SVG](../runs/samsung/EP01_descriptive/20261022T070701_403388Z/figures/sensitivity/04_raw_closes_since_2019.svg) |
| EP01_F05 | `05_trading_activity.png` / `.svg` | [PNG](../runs/samsung/EP01_descriptive/20261022T070701_403388Z/figures/main/05_trading_activity.png) · [SVG](../runs/samsung/EP01_descriptive/20261022T070701_403388Z/figures/main/05_trading_activity.svg) | [PNG](../runs/samsung/EP01_descriptive/20261022T070701_403388Z/figures/sensitivity/05_trading_activity.png) · [SVG](../runs/samsung/EP01_descriptive/20261022T070701_403388Z/figures/sensitivity/05_trading_activity.svg) |
| EP01_F06 | `06_rolling_discount_volatility.png` / `.svg` | [PNG](../runs/samsung/EP01_descriptive/20261022T070701_403388Z/figures/main/06_rolling_discount_volatility.png) · [SVG](../runs/samsung/EP01_descriptive/20261022T070701_403388Z/figures/main/06_rolling_discount_volatility.svg) | [PNG](../runs/samsung/EP01_descriptive/20261022T070701_403388Z/figures/sensitivity/06_rolling_discount_volatility.png) · [SVG](../runs/samsung/EP01_descriptive/20261022T070701_403388Z/figures/sensitivity/06_rolling_discount_volatility.svg) |
| EP01_F07 | `flagged_discount_windows.png` / `.svg` | [PNG](../runs/samsung/EP01_descriptive/20261022T070701_403388Z/episodes/flagged_discount_windows.png) · [SVG](../runs/samsung/EP01_descriptive/20261022T070701_403388Z/episodes/flagged_discount_windows.svg) | Local inspection |

Exact non-figure files:

- [episodes/flagged_episode_comparison.csv](../runs/samsung/EP01_descriptive/20261022T070701_403388Z/episodes/flagged_episode_comparison.csv)
- [episodes/REVIEW.md](../runs/samsung/EP01_descriptive/20261022T070701_403388Z/episodes/REVIEW.md)
- [episodes/source_rows_around_flags.csv](../runs/samsung/EP01_descriptive/20261022T070701_403388Z/episodes/source_rows_around_flags.csv)
- [provenance/environment.json](../runs/samsung/EP01_descriptive/20261022T070701_403388Z/provenance/environment.json)
- [provenance/METHODOLOGY.md](../runs/samsung/EP01_descriptive/20261022T070701_403388Z/provenance/METHODOLOGY.md)
- [provenance/source_inventory.json](../runs/samsung/EP01_descriptive/20261022T070701_403388Z/provenance/source_inventory.json)
- [provenance/validation.txt](../runs/samsung/EP01_descriptive/20261022T070701_403388Z/provenance/validation.txt)
- [provenance/worktree.patch](../runs/samsung/EP01_descriptive/20261022T070701_403388Z/provenance/worktree.patch)
- [README.md](../runs/samsung/EP01_descriptive/20261022T070701_403388Z/README.md)
- [tables/annual_distributions.csv](../runs/samsung/EP01_descriptive/20261022T070701_403388Z/tables/annual_distributions.csv)
- [tables/field_coverage.csv](../runs/samsung/EP01_descriptive/20261022T070701_403388Z/tables/field_coverage.csv)
- [tables/flagged_dates.csv](../runs/samsung/EP01_descriptive/20261022T070701_403388Z/tables/flagged_dates.csv)
- [tables/issue_inventory.csv](../runs/samsung/EP01_descriptive/20261022T070701_403388Z/tables/issue_inventory.csv)
- [tables/largest_changes.csv](../runs/samsung/EP01_descriptive/20261022T070701_403388Z/tables/largest_changes.csv)
- [tables/measures_main.csv](../runs/samsung/EP01_descriptive/20261022T070701_403388Z/tables/measures_main.csv)
- [tables/measures_sensitivity.csv](../runs/samsung/EP01_descriptive/20261022T070701_403388Z/tables/measures_sensitivity.csv)
- [tables/raw_quality.json](../runs/samsung/EP01_descriptive/20261022T070701_403388Z/tables/raw_quality.json)
- [tables/summary.json](../runs/samsung/EP01_descriptive/20261022T070701_403388Z/tables/summary.json)

Every snapshot/support file and hash is retained in the manifest and artifact catalog.

## Research code and registries

- [Descriptive entry point](../scripts/run_samsung_descriptive.py)
- [Independent saved-output verifier](../scripts/verify_samsung_pack.py)
- [Plot and calculation module](../src/samsung_research/descriptive.py)
- [Index and log generation](../src/samsung_research/navigation.py)
- [Existing source validation](../src/samsung_research/e01.py)
- [Pack configuration](../configs/samsung_descriptive.json)
- [Canonical methodology JSON](../methodology/methodology.json) and [schema](../methodology/schema.json)
- [Source inventory](../research/source_inventory.json), [experiment record](../research/experiments/EP01.json), [run reviews](../research/run_reviews.json)
- [Descriptive checks](../tests/check_descriptive.py) and [source checks](../tests/check_samsung_e01.py)

## Archived input-validation runs

Prior adjusted-price panels under methodology 1.0.0 are superseded/deferred, not current evidence. Older raw-discount results remain dated observations. No old directory was moved.

### samsung_E01_20261022T061948_834365Z

Methodology 1.0.0 · [manifest](../runs/samsung_E01_20261022T061948_834365Z/manifest.json)

- [DATA_QUALITY_REPORT.md](../runs/samsung_E01_20261022T061948_834365Z/DATA_QUALITY_REPORT.md)
- [discontinuity_review.csv](../runs/samsung_E01_20261022T061948_834365Z/discontinuity_review.csv)
- [discount_and_indexed_prices.png](../runs/samsung_E01_20261022T061948_834365Z/discount_and_indexed_prices.png) — superseded adjusted-price panel
- [discount_and_indexed_prices.svg](../runs/samsung_E01_20261022T061948_834365Z/discount_and_indexed_prices.svg) — superseded adjusted-price panel
- [discount_history.png](../runs/samsung_E01_20261022T061948_834365Z/discount_history.png)
- [discount_history.svg](../runs/samsung_E01_20261022T061948_834365Z/discount_history.svg)
- [field_coverage.csv](../runs/samsung_E01_20261022T061948_834365Z/field_coverage.csv)
- [paired_daily.csv](../runs/samsung_E01_20261022T061948_834365Z/paired_daily.csv)
- [summary.json](../runs/samsung_E01_20261022T061948_834365Z/summary.json)

### samsung_E01_20261022T062205_061875Z

Methodology 1.0.0 · [manifest](../runs/samsung_E01_20261022T062205_061875Z/manifest.json)

- [DATA_QUALITY_REPORT.md](../runs/samsung_E01_20261022T062205_061875Z/DATA_QUALITY_REPORT.md)
- [discontinuity_review.csv](../runs/samsung_E01_20261022T062205_061875Z/discontinuity_review.csv)
- [discount_and_indexed_prices.png](../runs/samsung_E01_20261022T062205_061875Z/discount_and_indexed_prices.png) — superseded adjusted-price panel
- [discount_and_indexed_prices.svg](../runs/samsung_E01_20261022T062205_061875Z/discount_and_indexed_prices.svg) — superseded adjusted-price panel
- [discount_history.png](../runs/samsung_E01_20261022T062205_061875Z/discount_history.png)
- [discount_history.svg](../runs/samsung_E01_20261022T062205_061875Z/discount_history.svg)
- [field_coverage.csv](../runs/samsung_E01_20261022T062205_061875Z/field_coverage.csv)
- [paired_daily.csv](../runs/samsung_E01_20261022T062205_061875Z/paired_daily.csv)
- [summary.json](../runs/samsung_E01_20261022T062205_061875Z/summary.json)

### samsung_E01_20261022T064759_477554Z

Methodology 2.0.0 · [manifest](../runs/samsung_E01_20261022T064759_477554Z/manifest.json)

- [DATA_QUALITY_REPORT.md](../runs/samsung_E01_20261022T064759_477554Z/DATA_QUALITY_REPORT.md)
- [discontinuity_review.csv](../runs/samsung_E01_20261022T064759_477554Z/discontinuity_review.csv)
- [discount_history.png](../runs/samsung_E01_20261022T064759_477554Z/discount_history.png)
- [discount_history.svg](../runs/samsung_E01_20261022T064759_477554Z/discount_history.svg)
- [field_coverage.csv](../runs/samsung_E01_20261022T064759_477554Z/field_coverage.csv)
- [paired_daily.csv](../runs/samsung_E01_20261022T064759_477554Z/paired_daily.csv)
- [summary.json](../runs/samsung_E01_20261022T064759_477554Z/summary.json)

## Observation ledger

### O001

2026-10-22 · motivation · hypotheses: H0

Candidate mappings: gvkey 104604, preferred 01W/KR7005931001, common 02W/KR7005930003, local KRW


Next: Verify exported mapping against issuer ISIN/class information

### O002

2026-10-22T06:22:05Z · measurement concern · hypotheses: H0

Actual input ends 2025-01-31; 12 issues present, two local classes selected; 4949 matched valid dates, 237 union dates excluded, zero duplicate keys; 2012-10-03 common status 5 conflicts with positive volume/high/low

- [research/source_inventory.json](../research/source_inventory.json)

Next: Obtain r_prc_stat and independently reconcile 2012-10-03 plus calendar/missing-class dates

### O003

2026-10-22T06:22:05Z · supportive association · hypotheses: H0, H2

Both classes have split=50 and AJEXDI 50 to 1 on 2018-05-04, consistent with issuer split disclosure; adjusted-price division removes the mechanical split scale change


Next: Reconcile independent raw closes around split and obtain dated articles

### O004

2026-10-22T06:22:05Z · motivation · hypotheses: H1, H2, H3, H4, H5, H6, H7

Observed discount is positive on all 4949 matched dates: minimum 4.7808764940239% on 2021-09-09, maximum 45.79124579124579% on 2009-04-06, median 21.666666666666668%, endpoint 17.938931297709924%; visually the level changes substantially across periods


Next: Validate extremes against independent closes before interpreting economic mechanisms

### O005

2026-10-22T06:22:05Z · measurement concern · hypotheses: H0

Three matched-date discount moves exceed 5 percentage points (2008-11-28, 2008-12-01, 2015-10-30); one adjacent valid interval spans 11 calendar days ending 2017-10-10


Next: Independent close/calendar checks on flagged dates; no causal event attribution yet

### O006

2026-10-22T06:49:30.378927+00:00 · measurement concern · hypotheses: H0

User supplied vendor PRCSTD/CSHTRD/QUNIT definitions: code 10 permits changed price without volume; remove positive-volume gate. AJEXDI formula remains unresolved and panel is deferred.

- [docs/reference/data/WRDS_VENDOR_DEFINITIONS.md](../docs/reference/data/WRDS_VENDOR_DEFINITIONS.md)

Next: Reconcile contradictory carried-code observation and obtain underlying company adjustment definition

### O007

2026-10-22T06:49:30.378927+00:00 · motivation · hypotheses: H0, H7

New export has 52514 raw rows; 5367 matched valid dates; 266 union dates excluded; last discount 21.56028369%. All 48008 old rows agree, no old keys lost. QUNIT=1 for all 11259 selected rows. Eight checks passed; chart visually inspected.


Next: Independent quote/calendar validation, then user-directed descriptive follow-up; no causal interpretation

### O008

2026-10-22T06:49:30.378927+00:00 · motivation · hypotheses: H7

User confirms Barra access. Local loaders document percent Barra returns and shipped USSLOWL factor names. Existing FF helper shifts ascending factors by -1, which conflicts with its lag description. Factor geography, units and Korean-close alignment need verification.

- [src/sf_quant/data/factors.py](../src/sf_quant/data/factors.py)
- [src/sf_quant/data/_factors.py](../src/sf_quant/data/_factors.py)
- [src/sf_quant/data/fama_french.py](../src/sf_quant/data/fama_french.py)
- [src/sf_quant/research/ff_regression.py](../src/sf_quant/research/ff_regression.py)
- [docs/FACTOR_RESEARCH_NOTES.md](../docs/FACTOR_RESEARCH_NOTES.md)

Next: Audit source metadata/timestamps and specify discount-level versus change outcome before future regressions

### O_EP01_20261022T070352_803683Z

2026-10-22T07:04:01.013354+00:00 · motivation · hypotheses: H0, H3, H7

Descriptive pack produced: six main and six flag-exclusion figures plus local episode windows. Main 5367 discount observations vs 5363 sensitivity; rolling windows 5229 vs 5165. No causal or liquidity conclusion.

- [runs/samsung/EP01_descriptive/20261022T070352_803683Z/README.md](../runs/samsung/EP01_descriptive/20261022T070352_803683Z/README.md)
- [runs/samsung/EP01_descriptive/20261022T070352_803683Z/episodes/REVIEW.md](../runs/samsung/EP01_descriptive/20261022T070352_803683Z/episodes/REVIEW.md)
- [runs/samsung/EP01_descriptive/20261022T070352_803683Z/tables/summary.json](../runs/samsung/EP01_descriptive/20261022T070352_803683Z/tables/summary.json)
- [runs/samsung/EP01_descriptive/20261022T070352_803683Z/figures/main/01_discount_history.png](../runs/samsung/EP01_descriptive/20261022T070352_803683Z/figures/main/01_discount_history.png)
- [runs/samsung/EP01_descriptive/20261022T070352_803683Z/figures/main/02_annual_distributions.png](../runs/samsung/EP01_descriptive/20261022T070352_803683Z/figures/main/02_annual_distributions.png)
- [runs/samsung/EP01_descriptive/20261022T070352_803683Z/figures/main/03_daily_discount_changes.png](../runs/samsung/EP01_descriptive/20261022T070352_803683Z/figures/main/03_daily_discount_changes.png)
- [runs/samsung/EP01_descriptive/20261022T070352_803683Z/figures/main/04_raw_closes_since_2019.png](../runs/samsung/EP01_descriptive/20261022T070352_803683Z/figures/main/04_raw_closes_since_2019.png)
- [runs/samsung/EP01_descriptive/20261022T070352_803683Z/figures/main/05_trading_activity.png](../runs/samsung/EP01_descriptive/20261022T070352_803683Z/figures/main/05_trading_activity.png)
- [runs/samsung/EP01_descriptive/20261022T070352_803683Z/figures/main/06_rolling_discount_volatility.png](../runs/samsung/EP01_descriptive/20261022T070352_803683Z/figures/main/06_rolling_discount_volatility.png)
- [runs/samsung/EP01_descriptive/20261022T070352_803683Z/figures/sensitivity/01_discount_history.png](../runs/samsung/EP01_descriptive/20261022T070352_803683Z/figures/sensitivity/01_discount_history.png)
- [runs/samsung/EP01_descriptive/20261022T070352_803683Z/figures/sensitivity/02_annual_distributions.png](../runs/samsung/EP01_descriptive/20261022T070352_803683Z/figures/sensitivity/02_annual_distributions.png)
- [runs/samsung/EP01_descriptive/20261022T070352_803683Z/figures/sensitivity/03_daily_discount_changes.png](../runs/samsung/EP01_descriptive/20261022T070352_803683Z/figures/sensitivity/03_daily_discount_changes.png)
- [runs/samsung/EP01_descriptive/20261022T070352_803683Z/figures/sensitivity/04_raw_closes_since_2019.png](../runs/samsung/EP01_descriptive/20261022T070352_803683Z/figures/sensitivity/04_raw_closes_since_2019.png)
- [runs/samsung/EP01_descriptive/20261022T070352_803683Z/figures/sensitivity/05_trading_activity.png](../runs/samsung/EP01_descriptive/20261022T070352_803683Z/figures/sensitivity/05_trading_activity.png)
- [runs/samsung/EP01_descriptive/20261022T070352_803683Z/figures/sensitivity/06_rolling_discount_volatility.png](../runs/samsung/EP01_descriptive/20261022T070352_803683Z/figures/sensitivity/06_rolling_discount_volatility.png)

Next: Independent quotes/calendar for flagged episodes; choose next descriptive overlay once inputs arrive. No factors or returns yet.

### O_EP01_20261022T070352_803683Z_FLAGS

2026-10-22T07:04:01.013354+00:00 · measurement concern · hypotheses: H0

Four eligible review dates inspected locally; three >5pp moves and one 11-calendar-day interval. Code-5/volume conflict remains excluded. Local price/status consistency does not verify independent quotes or identify news causes.

- [runs/samsung/EP01_descriptive/20261022T070352_803683Z/episodes/REVIEW.md](../runs/samsung/EP01_descriptive/20261022T070352_803683Z/episodes/REVIEW.md)
- [runs/samsung/EP01_descriptive/20261022T070352_803683Z/episodes/flagged_episode_comparison.csv](../runs/samsung/EP01_descriptive/20261022T070352_803683Z/episodes/flagged_episode_comparison.csv)
- [runs/samsung/EP01_descriptive/20261022T070352_803683Z/episodes/source_rows_around_flags.csv](../runs/samsung/EP01_descriptive/20261022T070352_803683Z/episodes/source_rows_around_flags.csv)
- [runs/samsung/EP01_descriptive/20261022T070352_803683Z/tables/flagged_dates.csv](../runs/samsung/EP01_descriptive/20261022T070352_803683Z/tables/flagged_dates.csv)

Next: Independent quotes/calendar for flagged episodes; choose next descriptive overlay once inputs arrive. No factors or returns yet.

### O_EP01_20261022T070701_403388Z

2026-10-22T07:07:10.902219+00:00 · motivation · hypotheses: H0, H3, H7

Descriptive pack produced: six main and six flag-exclusion figures plus local episode windows. Main 5367 discount observations vs 5363 sensitivity; rolling windows 5229 vs 5165. No causal or liquidity conclusion.

- [runs/samsung/EP01_descriptive/20261022T070701_403388Z/README.md](../runs/samsung/EP01_descriptive/20261022T070701_403388Z/README.md)
- [runs/samsung/EP01_descriptive/20261022T070701_403388Z/episodes/REVIEW.md](../runs/samsung/EP01_descriptive/20261022T070701_403388Z/episodes/REVIEW.md)
- [runs/samsung/EP01_descriptive/20261022T070701_403388Z/tables/summary.json](../runs/samsung/EP01_descriptive/20261022T070701_403388Z/tables/summary.json)
- [runs/samsung/EP01_descriptive/20261022T070701_403388Z/figures/main/01_discount_history.png](../runs/samsung/EP01_descriptive/20261022T070701_403388Z/figures/main/01_discount_history.png)
- [runs/samsung/EP01_descriptive/20261022T070701_403388Z/figures/main/02_annual_distributions.png](../runs/samsung/EP01_descriptive/20261022T070701_403388Z/figures/main/02_annual_distributions.png)
- [runs/samsung/EP01_descriptive/20261022T070701_403388Z/figures/main/03_daily_discount_changes.png](../runs/samsung/EP01_descriptive/20261022T070701_403388Z/figures/main/03_daily_discount_changes.png)
- [runs/samsung/EP01_descriptive/20261022T070701_403388Z/figures/main/04_raw_closes_since_2019.png](../runs/samsung/EP01_descriptive/20261022T070701_403388Z/figures/main/04_raw_closes_since_2019.png)
- [runs/samsung/EP01_descriptive/20261022T070701_403388Z/figures/main/05_trading_activity.png](../runs/samsung/EP01_descriptive/20261022T070701_403388Z/figures/main/05_trading_activity.png)
- [runs/samsung/EP01_descriptive/20261022T070701_403388Z/figures/main/06_rolling_discount_volatility.png](../runs/samsung/EP01_descriptive/20261022T070701_403388Z/figures/main/06_rolling_discount_volatility.png)
- [runs/samsung/EP01_descriptive/20261022T070701_403388Z/figures/sensitivity/01_discount_history.png](../runs/samsung/EP01_descriptive/20261022T070701_403388Z/figures/sensitivity/01_discount_history.png)
- [runs/samsung/EP01_descriptive/20261022T070701_403388Z/figures/sensitivity/02_annual_distributions.png](../runs/samsung/EP01_descriptive/20261022T070701_403388Z/figures/sensitivity/02_annual_distributions.png)
- [runs/samsung/EP01_descriptive/20261022T070701_403388Z/figures/sensitivity/03_daily_discount_changes.png](../runs/samsung/EP01_descriptive/20261022T070701_403388Z/figures/sensitivity/03_daily_discount_changes.png)
- [runs/samsung/EP01_descriptive/20261022T070701_403388Z/figures/sensitivity/04_raw_closes_since_2019.png](../runs/samsung/EP01_descriptive/20261022T070701_403388Z/figures/sensitivity/04_raw_closes_since_2019.png)
- [runs/samsung/EP01_descriptive/20261022T070701_403388Z/figures/sensitivity/05_trading_activity.png](../runs/samsung/EP01_descriptive/20261022T070701_403388Z/figures/sensitivity/05_trading_activity.png)
- [runs/samsung/EP01_descriptive/20261022T070701_403388Z/figures/sensitivity/06_rolling_discount_volatility.png](../runs/samsung/EP01_descriptive/20261022T070701_403388Z/figures/sensitivity/06_rolling_discount_volatility.png)

Next: Independent quotes/calendar for flagged episodes; choose next descriptive overlay once inputs arrive. No factors or returns yet.

### O_EP01_20261022T070701_403388Z_FLAGS

2026-10-22T07:07:10.902219+00:00 · measurement concern · hypotheses: H0

Four eligible review dates inspected locally; three >5pp moves and one 11-calendar-day interval. Code-5/volume conflict remains excluded. Local price/status consistency does not verify independent quotes or identify news causes.

- [runs/samsung/EP01_descriptive/20261022T070701_403388Z/episodes/REVIEW.md](../runs/samsung/EP01_descriptive/20261022T070701_403388Z/episodes/REVIEW.md)
- [runs/samsung/EP01_descriptive/20261022T070701_403388Z/episodes/flagged_episode_comparison.csv](../runs/samsung/EP01_descriptive/20261022T070701_403388Z/episodes/flagged_episode_comparison.csv)
- [runs/samsung/EP01_descriptive/20261022T070701_403388Z/episodes/source_rows_around_flags.csv](../runs/samsung/EP01_descriptive/20261022T070701_403388Z/episodes/source_rows_around_flags.csv)
- [runs/samsung/EP01_descriptive/20261022T070701_403388Z/tables/flagged_dates.csv](../runs/samsung/EP01_descriptive/20261022T070701_403388Z/tables/flagged_dates.csv)

Next: Independent quotes/calendar for flagged episodes; choose next descriptive overlay once inputs arrive. No factors or returns yet.

### O_EP01_20261022T070701_403388Z_QA

2026-10-22T07:09:37.675044+00:00 · measurement concern · hypotheses: H0

All six main/sensitivity layouts inspected; corrected episode plot inspected. Independent saved-output arithmetic and local links verified; raw unchanged. Remaining quote/calendar flags are not resolved.

- [runs\samsung\EP01_descriptive\20261022T070701_403388Z\manifest.json](../runs\samsung\EP01_descriptive\20261022T070701_403388Z\manifest.json)
- [research/run_reviews.json](../research/run_reviews.json)

Next: Resolve flags with independent evidence; keep economic hypotheses provisional

