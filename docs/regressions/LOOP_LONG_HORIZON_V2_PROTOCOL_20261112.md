# LOOP-LH2 existing-sample stability protocol

Registered before execution on November 12, 2026. The original long-horizon
protocol and `configs/loop_long_horizon_v1.json` remain in force. This continuation
uses `configs/loop_long_horizon_v2.json` and a new ignored
`runs/loop_long_horizon/v2_JOBID/` directory. Baseline job 15293344, its verified
output hashes, original input files and all prior empirical verdicts are retained.

The three private receipts are checked against the acquisition handoff, delivery
JSON byte sizes and SHA-256 hashes, exact entry inventory, every entry hash,
path/symlink safety, existing snapshot bytes, and internal file manifests. Missing
archives or delivery JSONs are reported separately and do not block checks on the
existing samples. A failed integrity check stops use of the affected data. No
snapshot is overwritten and no return series is spliced.

Reconstruct all original forecast cases independently with calendar-date training
masks and numpy least squares. Retain each sample, pragmatic/strict coverage rule,
model, 24/60/120-month horizon, exact endpoint, matured-label training mask,
minimum observations and identical forecast origins. Blocked baseline fits are
retained, including every unavailable ten-year evaluation. No additional origin
is created by regularization.

For each original origin, compare OLS with ridge at a single fixed lambda of 1.
Minimize mean squared training error plus lambda times squared standardized
slopes; center and scale predictors using the training population SD only and
leave the intercept unpenalized. There is no penalty selection or ranking to
choose a deployment model. Verify ridge using an independent augmented-design
least-squares construction. Save origin-specific raw coefficients and coefficients
per training SD. Summarize first/last/range/sign transitions descriptively; their
changes can reflect the changing training distribution as well as instability.

Report persistence and training-mean comparisons, and nested comparisons on
identical origins. Report every nonempty `origin_grid modulo horizon` phase,
without selecting an anchor. Within a phase, holding-period interiors do not
overlap; boundary observations may be shared. Also report the fixed origin-year
groups through 2014, 2015–2019 and 2020 onward. Calendar-group outcomes can cross
group boundaries and overlap; these groups are descriptive regime diagnostics,
not independent holdouts. Small phase counts remain explicit. No p-values or
prospective/causal validation are claimed.

No backward sample extension is authorized by archive integrity alone. Qualify
each stable security/date interval for identity, exact source venue, currency and
quote scale, splits/receipt ratio, missing/status flags and corporate transitions.
Keep pre-Xetra VW quarantined; separate Novo predecessors and Nasdaq from the
exact NYSE receipt; do not invent pre-2005 positive Hyundai third-preferred
prices. Preserve raw distribution duplicates, dated identifiers, local/US split
clocks, fee effective dates and publication dates. Unknown structural publication
dates cannot enter historical forecasts. The undelivered structural supplement
does not block this existing-sample batch.

Per-model/group private forecast and coefficient files, atomic progress, frozen
executed source/config metadata, input hashes and an output manifest preserve
completed work. Public outputs contain reusable code and aggregate diagnostics
only; monthly panels, individual origins, raw actions and crosswalk rows remain
in ignored private storage. No paused job is restarted.
