# LOOP-LH2 receipts and existing-sample stability, November 12, 2026

Existing-sample checks proceeded while the long-history and structural deliveries
were unavailable. Fixed regularization changes several retrospective loss
comparisons, but does not establish a universal correction model or prospective
prediction. The original LOOP-LH1 findings and all earlier scoped results remain
unchanged.

## Receipt and qualification decisions

Main was fetched and fast-forward synchronization reported already up to date;
the tracked worktree was initially clean. Work continues on
`data/loop-long-horizon-v2-20261112`. The ORC instruction symlink targets the
current `/apps` copy; development, storage, security, Python, software, Slurm and
performance guidance were read. Computation and substantial receipt I/O used
Slurm, leaving paused work untouched.

| Private delivery | Bytes | ZIP entries verified | Internal inventory files verified | Decision |
| --- | ---: | ---: | ---: | --- |
| November 11 descriptors | 1,756,250 | 95 | 68 | Verified against handoff and delivery JSON |
| November 12 daily/mapping | 23,824,061 | 46 | 45 | Verified against handoff and delivery JSON |
| Long-history follow-up v1 | Expected 648,953,971 | Expected 273 | Unavailable | ZIP and delivery JSON missing from documented transfer directory |

Both available archives passed expected SHA-256 and byte size, exact entry
inventory, every entry hash, path/type/symlink checks, existing snapshot hashes,
and internal inventories. Their README, collection review, coverage audits,
source inventories and private `SSH_AGENT_PROMPT.md` were read. Neither older
archive contains a file named `REMOTE_AGENT_HANDOFF.md`. The descriptor internal
manifest uses Windows separators; these were normalized only when resolving its
internal references, with strict POSIX ZIP/delivery-path validation retained.
No delivered source or prior result was overwritten.

Missing private files:

- `data/acquisition/2026-11-12/loop_long_horizon_followup_2026-11-12_v1.zip`
- `data/acquisition/2026-11-12/loop_long_horizon_followup_2026-11-12_v1.delivery.json`

The long-history README, coverage/source matrices, selected identifier history,
duplicate-date audit and `REMOTE_AGENT_HANDOFF.md` therefore could not be read
or certified. The structural gap-closure supplement remains undelivered under
its separate-receipt requirement. These absences block affected extensions, not
the completed existing-sample checks.

**Zero new security/date intervals were released.** Before extension, qualify
identity, currency/quote units, split/receipt ratios, status/missing prices,
corporate transitions and exact source venue. Pre-Xetra Volkswagen remains
quarantined. Novo predecessors, demerger and Nasdaq observations remain separate
from the exact NYSE receipt. No positive pre-2005 Hyundai third-preferred price
is presumed. The reported 56,634 Global and 6,843 CRSP incremental raw rows are
handoff expectations, not locally verified counts. Actual qualified endpoints
and matured labels must determine 24/60/120-month eligibility.

The existing mapping exceptions, quote-status/venue limitations, Shell scale
assumption, local/US split clocks, receipt-ratio assumptions and class boundaries
remain in force. Raw corporate-action duplicates are preserved. No adjusted or
spliced return series was constructed. No annual structural fact, fee or payout
was added at a historical origin; unknown publication dates remain retrospective.

## Frozen comparison

Protocol: [version 2](LOOP_LONG_HORIZON_V2_PROTOCOL_20261112.md), configuration
`configs/loop_long_horizon_v2.json`. Main run: Slurm `15307902`, private output
`runs/loop_long_horizon/v2_15307902/`. The earlier attempt `15307895` stopped
before estimation on the internal Windows-path convention and is preserved.

All 13,695 baseline forecasts were reconstructed independently with calendar-date
training masks and numpy least squares; maximum discrepancy was 3.35e-12
percentage points. Exactly 13,695 ridge forecasts use the same samples, coverage
rules, features, origins and matured-label training sets. The single penalty
lambda=1 was fixed before execution, with training-only population-SD scaling
and an unpenalized intercept. Independent augmented-design reconstruction differs
by at most 2.28e-13 percentage points. No penalty was selected from test losses.

All original baseline output hashes and source input hashes passed. Baseline
blocked fits are copied privately, including the absence of ten-year forecast
evaluation. Missing history remains insufficient evidence, rather than a null.
Five numerical/chronology checks and synthetic receipt/path/mutation checks
passed. Origin-specific forecasts, raw and standardized coefficients, every
nonoverlap phase, fixed calendar periods and recoverable group files stay private.

Verification job `15308021` passed all 10,608 overall/phase/calendar score rows,
784 coefficient-drift summaries, 174 nested comparisons, identical-origin checks,
descriptor review counts and the portable daily audit controls. Its receipt is
`runs/loop_long_horizon/v2_15307902/verification_v2/AUDIT.json`. Earlier audit
`15308001` passed the aggregate and daily controls before the descriptor reviewer
rejected output outside its bundle. The retry used an isolated descriptor copy,
reused the completed daily audit after checking its raw hashes, and preserved
the earlier attempt. Neither failure changed estimates or delivered sources.
No independent-agent review is claimed. Main computation took 43 seconds with
about 112 MiB peak RSS; the successful final verification took 34 seconds.

Public aggregates: [forecast scores](LOOP_LONG_HORIZON_V2_SCORECARD_20261112.csv)
and [coefficient drift](LOOP_LONG_HORIZON_V2_DRIFT_20261112.csv).

## Main findings

For LH-LEVEL, the number of samples beating persistence is identical under
pragmatic and strict coverage:

| Horizon | Original OLS | Fixed ridge | Ridge improves OLS, pragmatic / strict |
| --- | ---: | ---: | ---: |
| 24 months | 4/11 | 6/11 | 7/11 / 7/11 |
| 60 months | 4/11 | 3/11 | 6/11 / 7/11 |

Improving OLS does not necessarily beat persistence. For a single standardized
predictor, this ridge penalty halves the OLS slope and blends its prediction
equally with the training mean. It provides a fixed shrinkage sensitivity,
not evidence that parameters are stable. The state model's ridge comparison
beats persistence in 6/11 samples at both horizons and both coverage rules;
the universal prediction claim remains unsupported.

VW's pragmatic 24-month LH-LEVEL OLS slope starts at +1.287, reaches -2.559,
and ends at -0.819, with one sign transition. Ridge reduces its persistence
R-squared loss from -7.208 to -1.426 but still loses substantially. At 60 months,
VW ridge worsens R-squared from -0.076 to -2.608. These outcomes are retained.

Novo's pragmatic LH-LEVEL R-squared is 0.404 OLS versus 0.309 ridge at 24 months,
and 0.162 versus 0.175 at 60 months. Strict coverage also remains positive for
both methods/horizons. Its pragmatic discount slope remains negative: the OLS
range is -1.603 to -0.971 at 24 months and -1.460 to -0.883 at 60 months.
Negative slopes and positive pooled loss comparisons remain descriptive evidence.

Every nonempty nonoverlapping phase was retained; no favorable anchor was
selected. Novo's pragmatic two-year OLS phase R-squared ranges from -0.329 to
0.684 with 7–8 forecasts per phase; fixed ridge ranges from 0.103 to 0.596.
Strict two-year ridge phases also remain positive, with only 5–8 forecasts.
Five-year phases contain just 1–2 outcomes each and have both positive and
negative loss comparisons under both methods and coverage rules. Large negative
phase R-squared values can arise when persistence loss is nearly zero; the
private tables retain RMSE and counts for interpretation. Phases share data and
cannot be counted as independent experiments.

The prespecified through-2014 / 2015–2019 / 2020-onward origin groups retain
all observations. Novo's pragmatic two-year OLS R-squared is positive in all
three groups (0.336 / 0.376 / 0.441). Its five-year OLS comparisons are
-0.318 / 0.215 / 0.219; fixed ridge gives 0.190 / 0.214 / 0.136. These are
overlapping retrospective diagnostics; outcomes can cross calendar boundaries.

The original activity result is reproduced: OLS activity improves none of the
11 two-year matched state comparisons. Under fixed ridge it improves 4/11
pragmatic and 5/11 strict comparisons, and 5/11 pragmatic five-year comparisons
(5/10 strict). This qualifies the regularization sensitivity; it does not erase
the original specification's negative finding or establish a liquidity mechanism.

B01/B02 remain mixed, specification-dependent retrospective evidence. Novo
remains a candidate for exact-venue, ratio/clock, cash-cost and future-origin
challenges. M01/M02 retain their interval qualification gates. L01 remains a
proxy/specification test, while supply, ownership, control and payout branches
await independently dated mechanism evidence. No deployable forecast or causal
mechanism is validated by this batch.
