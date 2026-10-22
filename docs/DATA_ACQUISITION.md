# Samsung data acquisition and remaining validation

Latest figures: [EP01 descriptive pack](../runs/samsung/EP01_descriptive/20261022T070701_403388Z/README.md).
The remaining inputs below are unchanged by plotting; flags are shown and
sensitivity excludes them without closing gaps. [Hypothesis tree](HYPOTHESES.md)
and [research log](RESEARCH_LOG.md) provide the full output index.

## Current specification 2.0.0

The active immutable extract is
`docs/reference/data/samsung_data/samsung_2005-20261020.csv`, SHA-256
`c64a9cdbba02ee7d70cd3fa4b0af14e0540d0beab70d3d55132f333fb11ba8bb`.
Observed history reaches 2026-10-20. The older input and runs remain preserved.
All 48,008 overlapping raw rows agree field by field. Neither raw file is
overwritten. Both files and all run outputs remain excluded from Git.

User-supplied vendor definitions are saved in
`docs/reference/data/WRDS_VENDOR_DEFINITIONS.md`. PRCSTD, CSHTRD and QUNIT
meanings are now supplied; do not request them again. QUNIT=1 across all
11,259 selected local rows. Code 5 is excluded; code 10 is not gated on positive
volume because the vendor permits price changes without reported volume.
AJEXDI's underlying company-level formula remains unresolved; adjusted-price
panels and adjusted-return calculations are deferred.

Still needed: independent session/suspension calendar and raw quote checks on
flagged/extreme dates, explanation of common 2012-10-03 status/volume conflict,
exchange/type reference tables, original export settings/retrieval date,
complete dated class terms/actions and the underlying adjustment definition.
The October-2026 extension is now present; no further extension is requested.

Barra access is user-confirmed. Local loaders and the Fama–French helper were
reviewed; see `docs/FACTOR_RESEARCH_NOTES.md` for geography, units and timing
issues to resolve before the future regression stage. No regression has run.

The following initial-acquisition notes describe the archived v1 input and
superseded requests. Use this current section for remaining work.

## Archived version 1 acquisition notes

The immutable local input is
`docs/reference/data/samsung_data/samsung_05-26.csv`. Its SHA-256 is
`bee836dd98b021ce17e3692e71cb72eba1565de6abc59b56274d2697cc9d2924`.
The file and `runs/` are excluded from Git. The raw file was untracked when
inspected. Nothing was uploaded, published, staged or committed.

Canonical field/source inventory: `research/source_inventory.json`.
Run-specific field missingness and usable dates: `field_coverage.csv`,
`issue_inventory.csv`, and `summary.json` inside the E01 run directory.

## What is present

The export has 48,008 rows, 30 fields and 12 gvkey/iid issues. Only 01W and 02W
are the requested local pair; overseas listings are excluded. Exported ISINs
match Samsung's official class mapping. Both local series span 2005-01-03 to
2025-01-31. Neither the filename nor the date of download extends coverage.

## Smallest remaining validation package

1. From the same WRDS query, save the date range, filters, selected fields,
   adjustment/export settings and actual download date. Keep original bytes.
2. Export `r_prc_stat` code descriptions for 5 and 10, `r_ex_codes` for 248,
   `r_issuetyp` for 0 and 1, and security-master descriptors for gvkey 104604,
   iids 01W/02W. Save the actual table/column names displayed by your account.
3. Save WRDS help for PRCCD, QUNIT, AJEXDI, PRCSTD, CSHTRD, SPLIT and SPLITF.
   In particular confirm whether CSHTRD is shares or lots, venue scope,
   adjustment direction/event coverage and the carried-price rule. Public WRDS
   documentation redirected to login; no authenticated dictionary was obtained.
4. Obtain an official KRX trading-session and Samsung suspension calendar.
   Fifty-four weekdays are absent both classes; do not classify them as missing
   trading sessions without that calendar. Also check seven dates with only
   one class row: 2007-11-16, 2008-02-06/07/08, 2008-04-09, 2008-04-30,
   2008-09-22.
5. Independently export raw closes for BOTH local classes on 2005-01-03,
   2009-04-06, 2012-10-03, 2018-04-27, 2018-05-04, 2021-09-09 and
   2025-01-31; also 2008-11-27/28, 2008-12-01, 2015-10-29/30 and
   2017-09-29/2017-10-10. Include source, units, status and timestamp.
   These cover the base/end, extrema, split, contradictory carried code,
   flagged large moves and a long interval. No independent price match is
   claimed yet.
6. If the intended sample includes 2025-02 through 2026, export the missing
   extension for the same issues and fields. Preserve as a NEW immutable raw
   file and version the source/configuration; do not overwrite this extract.

Full dated class terms and dividend-event conventions remain unresolved before
interpreting the gap as vote value or building total-return wealth. Fundamental,
buyback, lending and flow datasets are later dependencies. This milestone does
not start those experiments, models or backtests.

## Local reproduction

Use the project's existing Python environment; install the research dependencies
from `research/requirements.lock` in a fresh environment if necessary. Existing
`uv.lock` remains unchanged. Each run snapshots Python/package versions, the
lockfiles, code, source inventory, methodology, input hash and dirty worktree.

```powershell
.venv/Scripts/python.exe -m unittest discover -s tests -p 'check_*.py'
.venv/Scripts/python.exe scripts/run_samsung_e01.py
```

`--raw PATH`, `--output-root PATH` and `--config PATH` support local paths.
Registered default input hashes are enforced; new raw datasets need a new source
version. Every analytical run creates a new directory. To regenerate the
documentation after an explicit JSON methodology revision:

```powershell
.venv/Scripts/python.exe scripts/run_samsung_e01.py --sync-methodology
```


## Version 2 completed run

`runs/samsung_E01_20261022T064759_477554Z/` contains the current raw-price chart, coverage report, overlap audit, methodology snapshots and validation log. There are 5,367 matched dates through 2026-10-20; 266 excluded union dates; no overlap revisions. Eight checks passed and chart inspected. Both raw files unchanged. Adjustment panel and regressions deferred. Remaining flags are documented in the run report; prior sessions remain archived.
