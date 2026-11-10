# Samsung research log and artifact index

This is the clickable record of experiments and files. Canonical file catalog: [research/artifacts.json](../research/artifacts.json). Append-only [observations](../research/observations.jsonl) and [decisions](../research/decisions.jsonl) preserve prior claims and revisions. Raw and derived licensed artifacts remain local and Git-ignored.

[Hypothesis tree](HYPOTHESES.md) · [Methodology](METHODOLOGY.md) · [Run folders](../runs/README.md)

## Current descriptive packs

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


Next: Independent quotes/calendar for flagged episodes; choose next descriptive overlay once inputs arrive. No factors or returns yet.

### O_EP01_20261022T070352_803683Z_FLAGS

2026-10-22T07:04:01.013354+00:00 · measurement concern · hypotheses: H0

Four eligible review dates inspected locally; three >5pp moves and one 11-calendar-day interval. Code-5/volume conflict remains excluded. Local price/status consistency does not verify independent quotes or identify news causes.


Next: Independent quotes/calendar for flagged episodes; choose next descriptive overlay once inputs arrive. No factors or returns yet.

### O_EP01_20261022T070701_403388Z

2026-10-22T07:07:10.902219+00:00 · motivation · hypotheses: H0, H3, H7

Descriptive pack produced: six main and six flag-exclusion figures plus local episode windows. Main 5367 discount observations vs 5363 sensitivity; rolling windows 5229 vs 5165. No causal or liquidity conclusion.


Next: Independent quotes/calendar for flagged episodes; choose next descriptive overlay once inputs arrive. No factors or returns yet.

### O_EP01_20261022T070701_403388Z_FLAGS

2026-10-22T07:07:10.902219+00:00 · measurement concern · hypotheses: H0

Four eligible review dates inspected locally; three >5pp moves and one 11-calendar-day interval. Code-5/volume conflict remains excluded. Local price/status consistency does not verify independent quotes or identify news causes.


Next: Independent quotes/calendar for flagged episodes; choose next descriptive overlay once inputs arrive. No factors or returns yet.

### O_EP01_20261022T070701_403388Z_QA

2026-10-22T07:09:37.675044+00:00 · measurement concern · hypotheses: H0

All six main/sensitivity layouts inspected; corrected episode plot inspected. Independent saved-output arithmetic and local links verified; raw unchanged. Remaining quote/calendar flags are not resolved.

- [research/run_reviews.json](../research/run_reviews.json)

Next: Resolve flags with independent evidence; keep economic hypotheses provisional

### O_EP01_20261026T131848_234484Z

2026-10-26T13:19:09.327985+00:00 · motivation · hypotheses: H0, H3, H7

Descriptive pack produced: six main and six flag-exclusion figures plus local episode windows. Main 5367 discount observations vs 5363 sensitivity; rolling windows 5229 vs 5165. No causal or liquidity conclusion.

- [runs/samsung/RG/20261026T131821Z_setup/EP01/20261026T131848_234484Z/README.md](../runs/samsung/RG/20261026T131821Z_setup/EP01/20261026T131848_234484Z/README.md)
- [runs/samsung/RG/20261026T131821Z_setup/EP01/20261026T131848_234484Z/episodes/REVIEW.md](../runs/samsung/RG/20261026T131821Z_setup/EP01/20261026T131848_234484Z/episodes/REVIEW.md)
- [runs/samsung/RG/20261026T131821Z_setup/EP01/20261026T131848_234484Z/tables/summary.json](../runs/samsung/RG/20261026T131821Z_setup/EP01/20261026T131848_234484Z/tables/summary.json)
- [runs/samsung/RG/20261026T131821Z_setup/EP01/20261026T131848_234484Z/figures/main/01_discount_history.png](../runs/samsung/RG/20261026T131821Z_setup/EP01/20261026T131848_234484Z/figures/main/01_discount_history.png)
- [runs/samsung/RG/20261026T131821Z_setup/EP01/20261026T131848_234484Z/figures/main/02_annual_distributions.png](../runs/samsung/RG/20261026T131821Z_setup/EP01/20261026T131848_234484Z/figures/main/02_annual_distributions.png)
- [runs/samsung/RG/20261026T131821Z_setup/EP01/20261026T131848_234484Z/figures/main/03_daily_discount_changes.png](../runs/samsung/RG/20261026T131821Z_setup/EP01/20261026T131848_234484Z/figures/main/03_daily_discount_changes.png)
- [runs/samsung/RG/20261026T131821Z_setup/EP01/20261026T131848_234484Z/figures/main/04_raw_closes_since_2019.png](../runs/samsung/RG/20261026T131821Z_setup/EP01/20261026T131848_234484Z/figures/main/04_raw_closes_since_2019.png)
- [runs/samsung/RG/20261026T131821Z_setup/EP01/20261026T131848_234484Z/figures/main/05_trading_activity.png](../runs/samsung/RG/20261026T131821Z_setup/EP01/20261026T131848_234484Z/figures/main/05_trading_activity.png)
- [runs/samsung/RG/20261026T131821Z_setup/EP01/20261026T131848_234484Z/figures/main/06_rolling_discount_volatility.png](../runs/samsung/RG/20261026T131821Z_setup/EP01/20261026T131848_234484Z/figures/main/06_rolling_discount_volatility.png)
- [runs/samsung/RG/20261026T131821Z_setup/EP01/20261026T131848_234484Z/figures/sensitivity/01_discount_history.png](../runs/samsung/RG/20261026T131821Z_setup/EP01/20261026T131848_234484Z/figures/sensitivity/01_discount_history.png)
- [runs/samsung/RG/20261026T131821Z_setup/EP01/20261026T131848_234484Z/figures/sensitivity/02_annual_distributions.png](../runs/samsung/RG/20261026T131821Z_setup/EP01/20261026T131848_234484Z/figures/sensitivity/02_annual_distributions.png)
- [runs/samsung/RG/20261026T131821Z_setup/EP01/20261026T131848_234484Z/figures/sensitivity/03_daily_discount_changes.png](../runs/samsung/RG/20261026T131821Z_setup/EP01/20261026T131848_234484Z/figures/sensitivity/03_daily_discount_changes.png)
- [runs/samsung/RG/20261026T131821Z_setup/EP01/20261026T131848_234484Z/figures/sensitivity/04_raw_closes_since_2019.png](../runs/samsung/RG/20261026T131821Z_setup/EP01/20261026T131848_234484Z/figures/sensitivity/04_raw_closes_since_2019.png)
- [runs/samsung/RG/20261026T131821Z_setup/EP01/20261026T131848_234484Z/figures/sensitivity/05_trading_activity.png](../runs/samsung/RG/20261026T131821Z_setup/EP01/20261026T131848_234484Z/figures/sensitivity/05_trading_activity.png)
- [runs/samsung/RG/20261026T131821Z_setup/EP01/20261026T131848_234484Z/figures/sensitivity/06_rolling_discount_volatility.png](../runs/samsung/RG/20261026T131821Z_setup/EP01/20261026T131848_234484Z/figures/sensitivity/06_rolling_discount_volatility.png)

Next: Independent quotes/calendar for flagged episodes; choose next descriptive overlay once inputs arrive. No factors or returns yet.

### O_EP01_20261026T131848_234484Z_FLAGS

2026-10-26T13:19:09.327985+00:00 · measurement concern · hypotheses: H0

Four eligible review dates inspected locally; three >5pp moves and one 11-calendar-day interval. Code-5/volume conflict remains excluded. Local price/status consistency does not verify independent quotes or identify news causes.

- [runs/samsung/RG/20261026T131821Z_setup/EP01/20261026T131848_234484Z/episodes/REVIEW.md](../runs/samsung/RG/20261026T131821Z_setup/EP01/20261026T131848_234484Z/episodes/REVIEW.md)
- [runs/samsung/RG/20261026T131821Z_setup/EP01/20261026T131848_234484Z/episodes/flagged_episode_comparison.csv](../runs/samsung/RG/20261026T131821Z_setup/EP01/20261026T131848_234484Z/episodes/flagged_episode_comparison.csv)
- [runs/samsung/RG/20261026T131821Z_setup/EP01/20261026T131848_234484Z/episodes/source_rows_around_flags.csv](../runs/samsung/RG/20261026T131821Z_setup/EP01/20261026T131848_234484Z/episodes/source_rows_around_flags.csv)
- [runs/samsung/RG/20261026T131821Z_setup/EP01/20261026T131848_234484Z/tables/flagged_dates.csv](../runs/samsung/RG/20261026T131821Z_setup/EP01/20261026T131848_234484Z/tables/flagged_dates.csv)

Next: Independent quotes/calendar for flagged episodes; choose next descriptive overlay once inputs arrive. No factors or returns yet.

