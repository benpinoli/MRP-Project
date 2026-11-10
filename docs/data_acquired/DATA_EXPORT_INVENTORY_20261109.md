# MRP data export inventory

Inventory date: November 9, 2026  
Scope: MRP-Project source exports, LOOP exceptions, core-pair regressions, Samsung research, prior run folders, manifests, and accessible archives  
Method: read-only filesystem and metadata audit; no vendor query was rerun and no raw file was changed

This inventory distinguishes files verified on disk from files mentioned only in notes. It reports aggregate metadata only and does not reproduce licensed data rows, credentials, or restricted query results.

## Summary

The checkout contains the complete price inputs used by the three core-pair baseline regressions, the Samsung Compustat daily extract, the shared USSLOWL asset files used by the LOOP exception tests, and the expanded and archived Prosus/Tencent/Naspers bundle. It does not contain the exact foreign local legs for the nine outstanding LOOP comparisons, historical securities-lending data, executable tick/depth data, or intraday FX.

Only two executable queries survive beside the core-pair exports: the quarterly Compustat Global fundamentals query and the 2026 Compustat North America TSM ADR query. The original Global daily, annual fundamentals, CRSP daily/name-history, and Global descriptor queries are missing.

## 1. Core-pair source exports

All files below were verified under:

`data/acquisition/2026-11-09/core_pairs_raw/`

Their filesystem modification times are approximately November 9, 2026 at 18:39 Mountain Time. Those timestamps establish when the files were placed or copied here, not their original WRDS execution times.

### Compustat Global daily security export

Exact path:

`data/acquisition/2026-11-09/core_pairs_raw/core_pairs_compustat_global_daily.csv`

- Provider/table: S&P Compustat Global Daily; consistent with `comp_global_daily.g_secd`.
- Frequency: daily.
- Total rows: 23,864.
- Overall date range: 2005-01-03 through 2026-11-06.
- Securities:
  - SK Square, GVKEY/IID 350948/01W: 1,290 rows, 2021-11-29 through 2026-11-06.
  - SK Hynix, 204049/01W: 5,642 rows, 2005-01-03 through 2026-11-06.
  - Samsung Fire & Marine, 208765/01W: 5,642 rows, 2005-01-03 through 2026-11-06.
  - Samsung Electronics common, 104604/02W: 5,642 rows, 2005-01-03 through 2026-11-06.
  - TSMC Taiwan common, 201395/01W: 5,648 rows, 2005-01-03 through 2026-11-06.
- Main fields: GVKEY/IID, ISIN, SEDOL, company name, exchange and security status, currency, raw close/high/low, price-status code, quote unit, adjustment factor, volume, shares outstanding, dividends, splits, total-return factor, and announcement/record/payment dates.
- Original executable SQL: not found.
- Manifest and immutable hashes: `runs/core_pairs/baseline_20261109/manifest.json`.

### Compustat Global descriptors

| Exact path | Rows | Frequency/coverage | Main fields | Query status |
| --- | ---: | --- | --- | --- |
| `data/acquisition/2026-11-09/core_pairs_raw/g_company.csv` | 5 | Current/company descriptor export | GVKEY, company names, location, industry, incorporation, primary issues, IPO and delisting descriptors | Original query missing |
| `data/acquisition/2026-11-09/core_pairs_raw/g_security.csv` | 36 | Security descriptor records | GVKEY/IID, ticker, CUSIP, ISIN, SEDOL, exchange/country, status and security type | Original query missing |
| `data/acquisition/2026-11-09/core_pairs_raw/g_sec_history.csv` | 12 | Effective-dated history; effective dates 1900-01-01 through 2021-11-29 | GVKEY/IID, item, historical value, effective and through dates | Original query missing |

The descriptor exports cover the five core local companies and their associated issue records. They do not constitute complete depositary-bank or effective-dated ADR-ratio histories.

### Korean-pair fundamentals

| Exact path | Provider/table | Rows and coverage | Main fields | Query status |
| --- | --- | --- | --- | --- |
| `data/acquisition/2026-11-09/core_pairs_raw/sk_square_samsung_fire_fundamentals_annual.csv` | Compustat Global annual, apparently `g_funda` | 27 rows; 2005-03-31 through 2025-12-31 | Format/fiscal/publication fields, assets, equity, cash, debt, dividends, investments, liabilities and share fields | Original SQL missing |
| `data/acquisition/2026-11-09/core_pairs_raw/sk_square_samsung_fire_fundamentals_quarterly.csv` | `comp_global_daily.g_fundq` joined to `g_company` | 86 rows; 2008-03-31 through 2026-06-30 | Quarterly fiscal/publication fields, balance sheet, investments, debt, dividends and shares | SQL present beside export |

Exact quarterly query:

`data/acquisition/2026-11-09/core_pairs_raw/sk_square_samsung_fire_fundamentals_quarterly.sql`

Annual coverage by company is 22 Samsung Fire observations and 5 SK Square observations. Quarterly coverage is 68 Samsung Fire and 18 SK Square observations. Vendor `fdate` and `pdate` fields are present, but they do not independently prove the first public-release timestamp.

### TSM ADR exports

| Exact path | Provider/table | Rows and dates | Main fields | Query status |
| --- | --- | --- | --- | --- |
| `data/acquisition/2026-11-09/core_pairs_raw/tsm_crsp_daily_2005_2025.csv` | CRSP daily stock, PERMNO 85442 | 5,288; 2005-01-03 through 2025-12-31 | CUSIP/ticker/PERMCO, price, return, volume, daily bid/ask, shares outstanding and cumulative factors | Original query missing |
| `data/acquisition/2026-11-09/core_pairs_raw/tsm_crsp_daily_2026.csv` | CRSP daily stock, PERMNO 85442 | 187; 2026-01-02 through 2026-09-30 | Security descriptors, OHLC, returns, distributions, volume, trade count, bid/ask, shares/factors and market returns | Executable query missing |
| `data/acquisition/2026-11-09/core_pairs_raw/tsm_crsp_names.csv` | CRSP name/security history, PERMNO 85442 | 6 records; history begins 1997-10-08 | Effective dates, CUSIPs, exchange, ticker/symbol, issuer/security/share types and industry codes | Original query missing |
| `data/acquisition/2026-11-09/core_pairs_raw/tsm_compustat_na_daily_2026.csv` | `comp_na_daily_all.secd` joined to `company`, GVKEY/IID 201395/90 | 32; 2026-09-24 through 2026-11-06 | Date, ticker, CUSIP, exchange, adjustment factor, volume, currency, close and return factor | SQL present beside export |

Supporting non-executable query summary:

`data/acquisition/2026-11-09/core_pairs_raw/tsm_crsp_daily_2026_query_summary.pdf`

Exact Compustat North America SQL:

`data/acquisition/2026-11-09/core_pairs_raw/tsm_compustat_na_daily_2026.sql`

The five overlapping closes on September 24, 25, 28, 29 and 30, 2026 matched exactly. The completed panel uses CRSP through September 30 and Compustat North America from October 1 through November 6. CRSP-only returns and bid/ask fields remain missing after the handoff.

### Core FX exports

| Exact path | Provider/series | Rows and dates | Frequency and fields | Provenance gap |
| --- | --- | --- | --- | --- |
| `data/acquisition/2026-11-09/core_pairs_raw/DEXKOUS.csv` | FRED H.10 DEXKOUS, KRW per USD | 5,700; 2005-01-03 through 2026-11-06 | Daily date/value | Retrieval timestamp, URL parameters and vintage metadata absent |
| `data/acquisition/2026-11-09/core_pairs_raw/DEXTAUS.csv` | FRED H.10 DEXTAUS, TWD per USD | 5,700; 2005-01-03 through 2026-11-06 | Daily date/value | Retrieval timestamp, URL parameters and vintage metadata absent |

These are noon New York fixings. DEXTAUS therefore occurs after the Taiwan close and supports a retrospective same-calendar-date comparison, not a synchronized executable comparison.

### Ownership and filing observations

- `data/acquisition/2026-11-09/core_pairs_raw/2021-11-09_sk_hynix_major_shareholder_change.pdf`
- `data/acquisition/2026-11-09/core_pairs_raw/2026-02-13_samsung_electronics_shareholder_disclosure.pdf`
- `data/acquisition/2026-11-09/korean_ownership_observations.csv`: one SK Square/SK Hynix ownership observation, measured 2021-12-31 and published 2022-02-24.

These are individual observations, not the dated histories required for Korean NAV regressions.

### Core manifests and derived outputs

- Primary manifest: `runs/core_pairs/baseline_20261109/manifest.json`.
- Report: `runs/core_pairs/baseline_20261109/REPORT.md`.
- Coverage audit: `runs/core_pairs/baseline_20261109/coverage_join_audit.csv`.
- Identifier audit: `runs/core_pairs/baseline_20261109/identifier_matches.csv`.
- Fundamentals audit: `runs/core_pairs/baseline_20261109/fundamentals_coverage.csv`.
- Derived panel and estimates: `panels.csv`, `coefficients.csv`, `model_status.csv` in the same directory.

The manifest verifies unchanged SHA-256 hashes for all 17 raw files. The run outputs are derived data, not additional source exports.

## 2. Samsung source exports

### Compustat daily export

Exact path:

`src/sf_quant/data/samsung_2005-20261020.csv`

- Provider: S&P Compustat Global Security Daily via WRDS.
- Total rows: 52,514.
- Frequency: daily.
- Coverage: 2005-01-03 through 2026-10-20.
- Company: Samsung Electronics, GVKEY 104604.
- Contains 12 IIDs representing Korean local issues and foreign receipt/listing records.
- Local preferred 01W, ISIN KR7005931001: 5,630 rows.
- Local common 02W, ISIN KR7005930003: 5,629 rows.
- Main fields: GVKEY/IID/ISIN, exchange and issue type, currencies, unadjusted close/high/low, price status, quote unit, adjustment factor, volume, shares outstanding, splits, return factor, dividends, and announcement/record/payment dates.
- Original query: not recorded.
- Retrieval/export date: not recorded; first inspected 2026-10-22.
- SHA-256 and detailed field definitions: `research/source_inventory.json`.
- Supplied vendor definitions: `docs/reference/data/WRDS_VENDOR_DEFINITIONS.md`.

The source inventory records the v2 path as `docs/reference/data/samsung_data/samsung_2005-20261020.csv`, but that path is absent. The matching licensed file is the `src/sf_quant/data` file above. The older v1 `docs/reference/data/samsung_data/samsung_05-26.csv`, hash beginning `bee836`, was mentioned in the inventory but was not found anywhere under `/home/bpinoli/MRP`.

### Samsung factors and external state series

`data/regression/raw/barra/factors.csv`

- Source: `sf_quant.data.load_factors`, local source version 0.2.7.
- Rows: 5,493 daily observations.
- Dates: 2004-12-20 through 2026-10-20.
- Fields: date plus USSLOWL country, beta, value, size, momentum, liquidity, residual volatility, leverage, dividend yield, profitability and semiconductor factors.
- Exported UTC: 2026-11-02T05:00:07Z.
- Metadata: `data/regression/raw/barra/factors.csv.metadata.json`.
- Geography, units, timing and model vintage are explicitly unverified.

A duplicate run copy exists at:

`runs/samsung/RG/20261026T131821Z_setup/factors.production.csv`

External state files under `data/regression/raw/prediction_external_20261105/`:

| File | Provider | Rows and dates | Fields |
| --- | --- | --- | --- |
| `VIX_History.csv` | CBOE | 9,309; 1990-01-02 through 2026-11-04 | Date and VIX OHLC |
| `DEXKOUS.csv` | FRED | 5,948; 2004-01-02 through 2026-10-20 | Date and KRW/USD noon fixing |
| `DGS10.csv` | FRED | 5,948; 2004-01-02 through 2026-10-20 | Date and ten-year Treasury yield |

Exact source URLs, hashes, retrieval time and vintage limitations are recorded in:

`data/regression/raw/prediction_external_20261105/manifest.json`

### Samsung issuer documents and event sources

Official annual/interim PDFs are present at:

`data/regression/raw/long_horizon_issuer_20261105/issuer_2010.pdf` through `issuer_2025.pdf`.

The exact URL, byte count, SHA-256 and retrieval timestamp for each document are recorded in:

`data/regression/raw/long_horizon_issuer_20261105/download_manifest.json`

`issuer_2005.pdf` is mentioned only in the manifest because the download returned HTTP 403.

Six issuer-disclosure HTML files and parsed event metadata are under:

`data/regression/raw/samsung_events_20261105/`

The KRX source-qualification folder contains saved web responses and access evidence, but no economic export:

`runs/samsung/source_qualification_20261105/`

The attempted public short-sale request returned HTTP 403. No short-sale, investor-flow, foreign-ownership or securities-lending observations were acquired from it.

## 3. LOOP shared asset exports

The LOOP exception work used these 32 verified files:

`/home/bpinoli/groups/grp_quant/database/research/assets/assets_1995.parquet`

through

`/home/bpinoli/groups/grp_quant/database/research/assets/assets_2026.parquet`

- Provider/table: shared `grp_quant` USSLOWL research asset database. The precise original vendor/table/query is not documented in this project.
- Frequency: daily.
- Total source rows: 122,823,913.
- Overall dates: 1995-06-30 through 2026-11-06.
- The 2025 file ends 2025-10-16 and the 2026 file starts 2026-07-13; these are not continuous calendar-year partitions.
- Main fields: Barra ID, price, market capitalization, price source, currency, return, date, specific return, yield, total/specific risk, historical/predicted beta, daily and rolling volume, daily and rolling bid-ask spread, security/name/instrument/issuer/root identifiers, country and currency codes, ticker, CUSIP, Russell membership and universe flag.
- Original SQL/export log: not found.
- Exact file sizes and modification times: `runs/loop_exceptions/15208094/results/manifest.json`.

Per-file row counts:

```text
1995 1,212,587   1996 2,587,169   1997 2,926,806   1998 3,069,456
1999 3,034,599   2000 3,078,259   2001 3,064,601   2002 3,125,515
2003 3,134,493   2004 3,158,713   2005 3,034,083   2006 2,921,166
2007 2,952,654   2008 3,044,303   2009 3,111,844   2010 3,099,783
2011 4,018,716   2012 5,153,627   2013 5,119,311   2014 5,088,519
2015 5,084,076   2016 4,900,050   2017 4,680,901   2018 4,829,066
2019 4,859,761   2020 4,923,537   2021 5,133,843   2022 5,288,592
2023 5,308,850   2024 5,500,649   2025 4,408,068   2026 1,970,316
```

The final LOOP run selected 102,470 rows and found zero duplicate asset keys. Its manifest confirms that no licensed asset rows were written to the output directory.

### Securities found in the shared assets

Verified US share/proxy relationships include GOOGL/GOOG, Berkshire A/B, News Corp NWS/NWSA, Fox FOX/FOXA, Liberty LBRDA/LBRDK, Petrobras PBR/PBR.A, Volkswagen OTC VWAGY/VWAPY, Liberty Broadband/Charter, Brookfield BN/BAM, SoftBank/Arm, Prosus OTC/Tencent OTC, Naspers OTC/Prosus OTC, and Investor AB OTC/Atlas Copco OTC.

These are partial matches. They do not prove the exact foreign local line, effective-dated listing history, or ADR/ADS ratio.

### Nine outstanding exact LOOP comparisons

The shared asset exports do not fully cover the required exact securities for:

1. Alibaba Hong Kong primary/US ADR.
2. HDFC Indian primary/historical US ADR.
3. Shell primary/ADR through its historical structures.
4. Novo Nordisk Danish primary/US ADR.
5. BYD Shenzhen A/Hong Kong H.
6. Ping An Shanghai A/Hong Kong H.
7. Hyundai Korean common/exact preferred class.
8. Roche Swiss voting/nonvoting lines.
9. Volkswagen German common/preferred.

US OTC or proxy securities exist for some relationships, but they are not substitutes for the exact local lines or dated receipt-ratio histories.

## 4. Prosus/Tencent/Naspers bundle

Expanded bundle:

`data/prosus_tencent/prosus_tencent_data_bundle/`

Validated archive:

`data/prosus_tencent_validated_2026-11-02.zip`

- Archive members: 130.
- Archive size: 32,862,935 bytes.
- SHA-256: `6b3b09486c3f17673528e8fa486cf657d416e19d654ea75afe273116b5204eba`.
- The checksum matches `data/prosus_tencent_validated_2026-11-02.zip.sha256`.
- The ZIP is a packaged copy of the expanded bundle.

### Licensed WRDS exports with exact SQL

All are under `data/prosus_tencent/prosus_tencent_data_bundle/data/licensed/wrds/`.

| Export | Table | Rows and coverage | Query |
| --- | --- | --- | --- |
| `security_daily.csv` | `comp_global_daily.g_secd` joined to `g_company` | 5,589 rows, 2019-09-11 through 2026-10-30; Naspers 206059/02W, Tencent 270615/01W and Prosus 333645/02W, 1,863 rows each | `security_daily.sql` |
| `fundamentals_annual.csv` | `g_funda` joined to `g_company` | 16 rows; Naspers and Prosus, eight each, 2019-03-31 through 2026-03-31 | `fundamentals_annual.sql` |
| `fundamentals_quarterly.csv` | `g_fundq` joined to `g_company` | 57 rows; Naspers 29 and Prosus 28, 2019-03-31 through 2026-03-31 | `fundamentals_quarterly.sql` |

Download/export timestamps are recorded around November 2, 2026 at 20:37. Coverage and validation are documented in:

- `data/prosus_tencent/prosus_tencent_data_bundle/logs/wrds_validation.json`
- `data/prosus_tencent/prosus_tencent_data_bundle/logs/wrds_source_registry.csv`
- `data/prosus_tencent/prosus_tencent_data_bundle/wrds_acquisition_report.md`

### Public market, factor and FX exports

Under `data/prosus_tencent/prosus_tencent_data_bundle/data/raw/`:

| Export | Provider | Rows and dates | Main fields |
| --- | --- | --- | --- |
| `prosus_PRX_AS.csv` | Yahoo Finance via yfinance | 1,830; 2019-09-11 through 2026-11-02 | Date, adjusted/raw close, OHLC, dividends, splits, volume and provider symbol |
| `tencent_0700_HK.csv` | Yahoo Finance via yfinance | 1,757; same range | Same market fields |
| `naspers_NPN_JO.csv` | Yahoo Finance via yfinance | 1,786; same range | Same market fields |
| `euro_stoxx_50.csv` | Yahoo Finance via yfinance | 1,797; same range | Same market fields |
| `hang_seng.csv` | Yahoo Finance via yfinance | 1,757; same range | Same market fields |
| `msci_china_etf_proxy.csv` | Yahoo Finance via yfinance | 1,796; same range | Same fields plus capital gains |
| `ecb_fx_daily_long.csv` | ECB daily data API | 9,150; 2019-09-11 through 2026-11-02 | Date, CNY/GBP/HKD/USD/ZAR currency and foreign units per EUR |

Ken French raw source files:

- `ff5_europe_daily_source.csv`
- `ff5_asia_pacific_ex_japan_daily_source.csv`

Their processed daily panels contain 1,841 rows each, from 2019-09-11 through 2026-09-30. Exact download URLs, hashes and retrieval time are in:

`data/prosus_tencent/prosus_tencent_data_bundle/logs/collection_manifest.json`

### NAV, share and disclosure sources

- `data/disclosures/ProsusNAV-300926.xlsx`: 21 quarterly observations, 2021-09-30 through 2026-09-30; publication dates unverified.
- `data/disclosures/prosus-share-buyback.xlsx`.
- `data/disclosures/prosus-shares-in-issue-table.xlsx`.
- FY/HY disclosure PDFs from FY2020 through FY2026.
- Reorganization and Tencent distribution-event documents.
- Derived NAV, buyback, share-count and disclosure extractions under `data/processed/`.

Primary manifests and registries:

- `data/prosus_tencent/prosus_tencent_data_bundle/logs/package_manifest.json`
- `data/prosus_tencent/prosus_tencent_data_bundle/logs/collection_manifest.json`
- `data/prosus_tencent/prosus_tencent_data_bundle/logs/event_sources_manifest.json`
- `data/prosus_tencent/prosus_tencent_data_bundle/data/reference/source_registry.json`
- `data/prosus_tencent/prosus_tencent_data_bundle/logs/wrds_source_registry.csv`

## 5. Prior runs and archived bundles

The following contain derived panels, model estimates, audits and reports rather than additional original vendor exports:

- `runs/core_pairs/`: 33 CSVs, including baseline/validation panels and Prosus/Tencent panels.
- `runs/loop_exceptions/`: 22 CSVs of aggregate tests and coverage audits.
- `runs/hypothesis_resolution/`: 22 CSVs, including Samsung adjustment and TSMC timing panels.
- `runs/prosus_tencent/`: derived return-regression outputs.
- `runs/samsung/`: 326 CSVs and 203 JSON files across descriptive, regression, prediction, stability and long-horizon runs.

Samsung archives inspected without extraction:

- `runs/samsung/overnight_20261106/lhc_freeze_v1.tar.gz`
- `runs/samsung/overnight_20261106/preexisting_work.tar.gz`
- `runs/samsung/overnight_20261106/review_snapshot.tar.gz`

They contain code, documentation, frozen results and provenance. They do not contain another copy of the licensed Samsung daily source export.

## 6. Coverage of requested research needs

| Need | Inventory result |
| --- | --- |
| Core Compustat Global daily security export | Verified present |
| Core annual and quarterly fundamentals | Verified present; annual query missing, quarterly SQL present |
| Global company/security/history descriptors | Verified present; original queries missing |
| TSM CRSP daily 2005-2025 and 2026 | Verified present |
| TSM CRSP name history | Verified present |
| TSM saved CRSP queries | Missing; 2026 has only a query-summary PDF |
| TSM local/ADR ratio | Five Taiwan shares per ADS documented in methodology/configuration; no separate effective-dated depositary-ratio export found |
| Nine exact LOOP listing histories | Not present |
| Nine exact LOOP local daily panels | Not present |
| Effective-dated ADR ratios for the nine LOOP comparisons | Not present |
| Core daily prices, actions, dividends, volume and shares | Present in Compustat/CRSP |
| TSM ADR daily bid/ask | Present through CRSP cutoff 2026-09-30 |
| USSLOWL daily bid-ask-spread measure | Partly present; not executable quotes |
| Executable quotes, depth or tick data | No verified export found |
| Historical securities-lending fees, lendable quantity or utilization | No export found |
| Intraday FX | No export found |
| Daily FX fixings | FRED DEXKOUS/DEXTAUS and ECB daily data present |
| Korean dated ownership histories | Not present; isolated observations only |
| Historical KRX short/ownership panel | Not present; attempted anonymous access returned no data |

The Prosus acquisition report records denied access to `markit_msf_analytics_eqty_asia/euro/amer/other`; no borrow history was downloaded. Missing borrow observations must not be interpreted as zero fees or full availability.

## 7. Query, dictionary and manifest index

### Executable SQL verified present

- `data/acquisition/2026-11-09/core_pairs_raw/sk_square_samsung_fire_fundamentals_quarterly.sql`
- `data/acquisition/2026-11-09/core_pairs_raw/tsm_compustat_na_daily_2026.sql`
- `data/prosus_tencent/prosus_tencent_data_bundle/data/licensed/wrds/security_daily.sql`
- `data/prosus_tencent/prosus_tencent_data_bundle/data/licensed/wrds/fundamentals_annual.sql`
- `data/prosus_tencent/prosus_tencent_data_bundle/data/licensed/wrds/fundamentals_quarterly.sql`

### Core executable queries still missing

- Compustat Global daily-security export.
- Compustat Global annual fundamentals export.
- CRSP TSM daily 2005-2025 export.
- CRSP TSM daily 2026 export.
- CRSP TSM name-history export.
- Compustat Global company, security and security-history descriptor exports.

### Data dictionaries and provenance records

- `docs/reference/data/WRDS_VENDOR_DEFINITIONS.md`
- `research/source_inventory.json`
- `runs/core_pairs/baseline_20261109/manifest.json`
- `runs/loop_exceptions/15208094/results/manifest.json`
- `data/regression/raw/barra/factors.csv.metadata.json`
- `data/regression/raw/prediction_external_20261105/manifest.json`
- `data/regression/raw/long_horizon_issuer_20261105/download_manifest.json`
- `data/prosus_tencent/prosus_tencent_data_bundle/logs/package_manifest.json`
- `data/prosus_tencent/prosus_tencent_data_bundle/logs/collection_manifest.json`
- `data/prosus_tencent/prosus_tencent_data_bundle/logs/event_sources_manifest.json`
- `data/prosus_tencent/prosus_tencent_data_bundle/logs/wrds_source_registry.csv`
- `data/prosus_tencent/prosus_tencent_data_bundle/logs/wrds_validation.json`

Vendor reference-table exports such as Compustat `r_prc_stat`, exchange codes and issue-type dictionaries were not found.

## 8. Verified-present, note-only and uninspected locations

### Verified present

- All 17 core-pair source files listed in the baseline manifest.
- Samsung licensed daily export at `src/sf_quant/data/samsung_2005-20261020.csv`.
- Thirty-two USSLOWL annual asset Parquets.
- Prosus expanded bundle and matching validated ZIP.
- Samsung issuer reports, external state series and event documents.
- Five executable SQL files: two core and three Prosus.

### Mentioned in notes but not found

- `docs/reference/data/samsung_data/samsung_05-26.csv`.
- `docs/reference/data/samsung_data/samsung_2005-20261020.csv`.
- Original executable core queries listed above.
- Compustat reference-table dictionaries.
- Historical Markit lending data.
- Exact LOOP foreign local legs and receipt-ratio histories.
- Intraday FX and executable tick/depth data.

### Locations not fully checked

- No separate directory corresponding to the earlier `<upload directory>` placeholder was found under `/home/bpinoli/MRP`.
- The broader shared `grp_quant` database was accessible and its top-level research directories were listed, but only the `assets` files actually referenced by this project were scanned. Unrelated shared CRSP, risk and signal tables were not treated as MRP-Project exports.
- Authenticated WRDS, KRX, Bloomberg and Markit systems were not accessed.
- No hidden remote storage or temporary files from the prior lost SSH process were available from this checkout.

## 9. Interpretation boundary

Daily Compustat, CRSP, FRED and USSLOWL inputs support the completed descriptive price regressions. They do not by themselves support point-in-time NAV regressions, synchronized cross-market execution claims, or implementable trading results. Those require dated ownership/NAV histories, effective-dated receipt terms, publication clocks, borrow availability and fees, executable quotes, and synchronized or bounded FX observations.
