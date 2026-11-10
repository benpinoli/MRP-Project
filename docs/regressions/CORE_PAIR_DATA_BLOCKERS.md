# Core-pair regression data status and resolved blocker

As of November 9, 2026, the Samsung B01–B04 regressions are complete under
`runs/samsung/RG/20261103T010848_30613`. Prosus/Tencent has a completed return-
association suite under `runs/prosus_tencent/14992671`; a separate Samsung-style
normalized price-ratio sensitivity is configured in
`configs/core_pair_gap_regressions.v1.json`.

This note originally recorded the blocking export. That blocker was subsequently
resolved by the byte-preserved November 9 raw bundle under Git-ignored `data/`.
The completed audited run is `runs/core_pairs/baseline_20261109`, with tracked
results in `CORE_PAIR_BASELINE_RESULTS.md`. The shared USSLOWL `assets` table
still does not contain the Korean and Taiwanese local listings; the completed
panels therefore use the later dedicated Compustat Global/CRSP/FRED exports.

## Historical export request (now supplied)

The requested export was daily Compustat Global Security rows from
`comp_global_daily.g_secd` for
2005-01-01 through the latest common date for these listings:

- SK Square 402340 Korea and SK Hynix 000660 Korea.
- Samsung Fire & Marine 000810 Korea and Samsung Electronics 005930 Korea.
- TSMC 2330 Taiwan. TSM ADR is already identifiable in the US assets data, but
  using one vendor for both legs is preferable.

Retain at least `gvkey`, `iid`, `isin`, `sedol`, `conm`, `datadate`, `exchg`,
`secstat`, `epf`, `ajexdi`, `cshoc`, `cshtrd`, `curcdd`, `prccd`, `prcstd`,
`qunit`, `split`, `splitf`, `tpci`, `trfd`, and dividend/corporate-action date
fields. Also export a dated KRW/USD and TWD/USD source with documented fixing
time. Do not substitute current identifiers for historical mappings without an
effective-date audit.

For SK Square/SK Hynix and Samsung Fire/Samsung Electronics, a price ratio is
only a normalized descriptive gap until dated stake ownership, other assets,
cash, debt, liabilities, and economic share counts support a NAV denominator.
For TSMC, the run verifies five Taiwan common shares per ADS, identifier history,
and the 2026 CRSP/Compustat handoff. Close and FX clocks remain non-synchronous.

## Remaining provenance and structural inputs

The data are sufficient for the completed price baselines, but original
executable WRDS queries are still absent for Global daily prices, annual
fundamentals, CRSP 2005–2025, CRSP 2026, CRSP name history, and the Global
descriptor exports. FRED retrieval/vintage metadata are also absent. Korean NAV
tests remain blocked by dated ownership histories and point-in-time NAV inputs
for each pair, not by daily price coverage.
