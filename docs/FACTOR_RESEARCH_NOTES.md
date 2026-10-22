# Factor regression preparation

Updated 2026-10-22. User confirms Barra-factor access through this repository.
This session inspected local documentation and implementation only; no factor
regression, factor-data download, or data-coverage query has run.

## Verified repository interfaces

- `src/sf_quant/data/factors.py`: `load_factors(start, end, factors=None)` loads
  factor returns documented in percent, with inclusive dates. Divide by 100
  when a model requires decimal returns. `get_factors_columns()` queries the
  configured schema; `get_factor_names('style')` / `('sector')` return static
  name lists, not proof of live coverage.
- `src/sf_quant/data/_factors.py`: the shipped names use the `USSLOWL_` prefix,
  including VALUE, SIZE, MOMENTUM, LIQUIDTY, LEVERAGE and SEMICOND. Their names
  suggest a US model; actual model geography, currency, return definition and
  Korean relevance must be verified rather than assumed.
- `src/sf_quant/data/exposures.py`: separate security factor exposures from
  factor returns. Korean local security coverage and dated identifiers must be
  checked before any exposure-based attribution.
- `src/sf_quant/data/fama_french.py`: `load_fama_french(start,end)` loads
  `mkt_rf, smb, hml, rmw, cma, rf` through the configured view. `_views.py`
  passes stored values through without rescaling; units must be verified from
  source metadata rather than inferred from illustrative docstrings. Confirm factor geography/currency and
  sample coverage from the underlying source before interpreting coefficients.
- `src/sf_quant/data/_config.py`: loaders use ROOT/DATABASE configuration and
  the shared database. Do not paste credentials or environment values into
  research logs. This local-CSV chart requires no database connection.

The `.rst` files under `docs/reference/data/` are Sphinx entry points; function
docstrings and source contain the actual implementation.

## Timing concern in the existing regression helper

`src/sf_quant/research/ff_regression.py:run_ff_regression` is for portfolio
excess returns. It is not a drop-in model for a price discount. Its use of
`shift(-1)` on ascending factor dates assigns the next row's factor to the
current row, despite the docstring describing yesterday's factors. We have
not modified or used this helper. Before future use, explicitly test factor
alignment on known dates and choose timing appropriate to Korean closes and
the factor market's close. A US same-calendar-date return may not be known
at the Korean close.

## Future specification decisions

The observed preferred-share discount is a dimensionless price gap, not an
interest discount rate or portfolio return. Distinguish regressions explaining
discount levels, changes in percentage points, log-gap changes, and later
relative total returns. These have different interpretations and inference
requirements. No model is selected here.

Before estimation: audit factor coverage/units/geography/timestamps; define
the outcome and contemporaneous versus lagged question; handle Korean and
factor-market holidays explicitly; address serial dependence and persistent
levels; register the exploratory specification. Compare Barra and a suitably
matched Fama–French set as different models, not interchangeable factor names.
Total-return or adjusted-price outcomes remain blocked on their definitions.

This is a recorded next research direction, not an executed experiment or a
claim that factors explain the gap.
