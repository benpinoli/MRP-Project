# RG data contracts and organization

All paths in the config are repository-root-relative or absolute cluster paths. New `data/regression/` and all `runs/` content are ignored by Git. Keep licensed exports on authorized school storage. Do not put credentials or ROOT/DATABASE values in tracked metadata. No data download or upload is performed by this setup.

```text
data/regression/
  raw/barra/factors.csv                 # wide sf_quant export, immutable
  raw/barra/factors.csv.metadata.json   # export hash/date range, no credentials
  metadata/barra.json                  # completed metadata template
  metadata/factor_timing.csv           # return ends, availability timestamps
  metadata/factor_calendar.csv         # expected source dates from verified calendar
  metadata/sessions.csv                # date,close_utc for every proxy session
  metadata/mechanisms.json             # optional per-column provenance
  staged/mechanisms.csv                # optional, date + unlagged fields
runs/samsung/RG/<UTC-id>/
  frozen/                             # sources/config/docs/environment
  prepared/{panel.csv,alignment.csv,readiness.json,inputs.json}
  tasks.json                          # stable model×variant×window×HAC map
  results/task_00000/                  # exclusive directory per task
  REPORT.md, coefficients.csv, status.json
  logs/                               # %A_%a or job-ID Slurm logs
```

EP01's `tables/measures_main.csv`, `tables/measures_sensitivity.csv`, `manifest.json` and `provenance/source_inventory.json` are reused by exact path; preparation verifies their manifest hashes and enforces the registered raw-source hash against the inventory snapshot. Reproduce EP01 on the cluster if these ignored local outputs are not present. Main and sensitivity dates must match. The config intentionally points at the existing immutable run, not an ambiguous `latest` symlink.

## Required inputs

- `factors.csv`: unique ascending ISO `date`, selected numeric factor columns in original declared units. No duplicate dates, infinity, missing expected source dates or silent fill. The export helper uses `sf_quant.data.load_factors`; it does not create timing/geography metadata.
- `factor_timing.csv`: unique `date`, `period_end_utc`, `available_at_utc` in ISO-8601 with offset. `available_at_utc >= period_end_utc`. Every exported factor row needs timing. Timestamp conversion and special sessions must be verified; do not assign a single Seoul close time to the full history.
- `factor_calendar.csv`: one unique ISO `date` per expected source trading session over the full export date range. It must be independently sourced, not generated from the factor file itself. Metadata declares the inclusive covered range and source; preparation compares exact expected and observed dates within it. This detects a missing factor row rather than accidentally assigning a multi-session bin an incomplete shock.
- `sessions.csv`: unique ISO `date`, `close_utc` for every EP01 `observed_session=True` row, including invalid paired prices. Strictly increasing actual close timestamps; no duplicate dates. Must cover the full EP01 sample. Independent sessions absent from the proxy still need reconciliation before synchronized attribution claims.
- `barra.json`: complete [template](../../configs/barra_metadata.example.json): exact model, geography, currency, percent/decimal return units, vintage, timestamp/calendar source references, review confirmation and explicit US-sensitivity acknowledgement if applicable. Unknowns remain null and block preparation. Supported geography labels are Korea, global_with_Korea, US_sensitivity. Currency needs justification for the selected model and question; metadata review is substantive, not automatic verification by the program.

## Optional mechanisms

`mechanisms.csv`: unique date plus any of `spread_diff`, `log_turnover_ratio`, `retail_weight_diff`, `foreign_flow_diff`, `common_borrow_fee`, `buyback_diff`, `incremental_dividend`. Fields are unlagged values in [dictionary units](FACTORS.md). Rows may be missing and remain missing after a left join. Daily lagging occurs on the preserved session grid. The engine rejects nonnumeric nonempty fields; never use missing as zero. The metadata file must declare every supplied field, formula, source, unit, release/vintage policy, and confirm availability by that row's Korean close. Slow series may be carried from a genuinely public release by an audited upstream builder, with explicit staleness limits; the engine itself performs no filling. Revised history must be labeled retrospective and cannot support forecasting claims. This contract is a human provenance gate, not a claim of automatic point-in-time validation.

Changing inputs during preparation or fitting invalidates hashes. Jobs freeze code/configuration and copy the prepared panel before fitting. Original input files must remain unchanged during preparation; validate their hashes again before finishing. Each task verifies the prepared panel hash and writes exact sample endpoints. A malformed required input fails the preparation job; a missing optional block produces a blocked result with a reason. Do not collect blocked tests as null or zero effects.
