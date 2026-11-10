# Remaining core-pair baseline results

Run date: November 9, 2026  
Executable run: `runs/core_pairs/baseline_20261109`  
Configuration: `configs/core_pair_baselines.v1.json`

## Result in one paragraph

All three requested price panels and B00 mean-reversion baselines were completed through November 6, 2026. At HAC(20), the lag-gap coefficient was −0.01153 for SK Square/SK Hynix (p=0.0084, n=1,149), −0.00148 for Samsung Fire/Samsung Electronics (p=0.130, n=5,203), and −0.06905 for the TSMC ADR premium (p=4.15×10⁻²⁰, n=4,737). These are small in-sample price-adjustment associations: adjusted R² was 0.56%, 0.06%, and 3.42%, respectively. They are not NAV results, fair-value estimates, forecasts, causal estimates, or trading evidence.

## Samples and join losses

| Pair | Level dates | Change/regression dates | Actual B00 sample | Join/coverage notes |
| --- | ---: | ---: | --- | --- |
| SK Square / SK Hynix | 1,208 | 1,149 | 2021-11-30 to 2026-11-06 | SK Square starts 2021-11-29; 4,352 earlier Hynix-only dates; no Square-only dates |
| Samsung Fire / Samsung Electronics common | 5,386 | 5,203 | 2005-01-04 to 2026-11-06 | 5,642 dates exist for both legs; filtering uses reported-close `PRCSTD=10` and adjacent usable endpoints |
| TSMC local / ADR | 5,130 | 4,737 | 2005-01-04 to 2026-11-06 | 5,435 dates have both securities; 213 local-only, 62 ADR-only, and 50 paired-security dates lack same-day DEXTAUS |

The fixed older windows are correctly blocked for SK Square because the company was not listed. Samsung Fire/Samsung Electronics has n=2,428 / 1,171 / 1,604 in 2005–14 / 2015–19 / 2020–26. TSMC has n=2,196 / 1,072 / 1,469. Full coefficient and HAC(5/20/60) tables are in the run directory.

## Audit findings

- Identifier matches: Compustat Global GVKEY/IID pairs and descriptors match the requested active Korean/Taiwan listings and ISINs. CRSP name history identifies PERMNO 85442, ticker TSM, CUSIP 87403910, security subtype ADR, and issuer Taiwan Semiconductor Manufacturing Co Ltd.
- Duplicates: the Global GVKEY/IID/date keys are unique. The 2005–2025 CRSP export contains five duplicated dates (the five historical TSMC share-distribution dates); each duplicate is byte-identical at the row level and was naively deduplicated once. No conflicting date duplicates were repaired.
- Currencies: the Korean legs are KRW, TSMC local is TWD, and the ADR is USD. DEXKOUS was audited but is unnecessary for same-currency Korean ratios. DEXTAUS is TWD per USD.
- Corporate actions: Samsung Electronics has the 50:1 adjustment transition on May 4, 2018. TSMC has five historical share-distribution factor transitions from 2005–2009, mirrored closely in CRSP cumulative factors. Prices use `PRCCD/AJEXDI/QUNIT` or `DlyPrc/DlyCumFacPr`; no dividend total-return adjustment is made.
- Missing fields: Global close prices are complete for the selected securities, while volumes are missing mainly on `PRCSTD=5` dates. Same-day DEXTAUS is absent on 50 otherwise paired security dates. Compustat North America ADR continuation rows intentionally leave CRSP return, bid, and ask missing.
- Raw preservation: all 17 upload files retained their pre-run SHA-256 hashes after the run and remain excluded from Git under `/data`.

## ADR stitch and timing

The CRSP/Compustat North America overlap on September 24, 25, 28, 29, and 30, 2026 matched exactly numerically. CRSP is used through September 30; Compustat North America is used October 1–November 6, with a row-level `adr_source` tag.

The TSMC comparison uses five Taiwan common shares per ADS. The baseline converts the Taiwan leg with same-calendar-date DEXTAUS. Because FRED's fixing is noon New York—after the Taiwan close—the result is explicitly retrospective. The panel also preserves a latest-prior-fixing gap sensitivity, but it is not silently substituted into the frozen baseline.

## Fundamentals and Korean NAV status

Annual and quarterly exports were audited separately and were not used in the price regressions.

| Entity | Annual coverage | Annual vendor pdate | Quarterly coverage | Quarterly vendor pdate |
| --- | --- | --- | --- | --- |
| Samsung Fire (208765) | 22 rows, 2005-03-31 to 2025-12-31 | 19 present, 3 missing | 68 rows, 2008-03-31 to 2026-06-30 | 68 present |
| SK Square (350948) | 5 rows, 2021-12-31 to 2025-12-31 | 4 present, 1 missing | 18 rows, 2022-03-31 to 2026-06-30 | 18 present |

Vendor `fdate`/`pdate` coverage does not prove original public availability or revision vintage. Korean NAV regressions remain pending: commit `3666efa` and the supplied filings provide individual ownership observations, but neither Korean pair has the required dated ownership history.

## Handoff gaps

The quarterly fundamentals SQL and the Compustat North America ADR SQL are present. Missing original executable queries: Global daily prices, annual fundamentals, CRSP 2005–2025, CRSP 2026, CRSP name history, and Global company/security/history descriptors. The CRSP 2026 query-summary PDF is retained but is not executable SQL. FRED retrieval/vintage metadata are also absent. The supplied CRSP name-history file ends December 31, 2025; embedded identifiers in the 2026 CRSP daily export support the 2026 continuation.

Reproduce with:

```bash
.venv-rg/bin/python scripts/run_core_pair_baselines.py \
  --config configs/core_pair_baselines.v1.json \
  --output runs/core_pairs/<new-run-id>
```
