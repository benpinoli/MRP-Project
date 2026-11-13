# Scientific next experiments for long-horizon LOOP discount prediction

November 12, 2026. Analyst recommendation to the coordinating agent, based on
the [hypothesis tree](PREDICTION_MECHANISM_TREE.json),
[AR01–AR13 review](LOOP_ANALYST_REVIEW_20261112.md), and verified v4 diagnostics.
This is a proposed design, not a new estimation result. No computation was
launched and no canonical tree, ledger, model configuration or historical
verdict was modified by this review.

## Recommendation and boundary

Proceed with one tightly bounded statistical repair while acquiring the evidence
needed to challenge Novo's measurement. Do not choose between these by whichever
produces the best historical R-squared. A valid positive-price forecast is a
necessary mathematical condition; it does not validate the economic object or
identify a mechanism. Conversely, several additional fee notices cannot certify
the historical quote source or eliminate asynchronous-close effects.

The most discriminating addition to the immediate test is a **terminal-level
training-mean benchmark**. Our existing training-mean benchmark averages past
discount **changes**. Predicting the mean future discount **level** instead is
a different, economically relevant anchor. Novo's change-regression slopes
near minus one can reflect reversion to an almost constant terminal discount;
that can predict changes while adding little conditional information about the
future terminal level. Test that possibility before interpreting the state
coefficient as a richer predictive mechanism.

Execution order is below. Measurement qualification has greater epistemic
priority than a favorable model score; the first test can nevertheless proceed
immediately on the existing scoped samples while the acquisition is unresolved.

| Rank | Experiment | Scientific purpose | Feasibility now |
| --- | --- | --- | --- |
| 1 | One positive conditional-mean ratio model against three fixed benchmarks | Distinguish inadmissible linear extrapolation, a generic terminal anchor, and useful conditional state information | Existing qualified monthly panels; no new prices or structural features |
| 2 | Narrow Novo venue/unit/ratio qualification and synchronized-quote feasibility pilot | Challenge measurement as the explanation for the most consistent long-horizon candidate; assess a defensible older extension | Existing raw prehistory can be audited; missing source provenance/quotes require an entitled provider or exchange/issuer evidence |
| 3 | Prospective issuance and evaluation registry | Determine whether gains survive genuinely new origins and actual input-delivery timing | Registry can be built now; 24/60/120-month outcomes require real elapsed time |

## Experiment 1 — Positive conditional mean and the terminal-anchor rival

**Tree:** M01/M02, B01/B02; a new long-horizon functional-form question, not a
retroactive change to the archived short-horizon B04 verdict.

**Hypotheses and rivals.** The current discount state may contain information
about future relative prices beyond persistence. Rival one is unstable,
unconstrained extrapolation, exposed by 316 saved OLS forecast-variant cases
with impossible terminal discounts at or above 100. Rival two is a generic
terminal-level anchor rather than meaningful state-dependent information.
Both can coexist with measurement error and exposed-history selection.

**Single candidate.** For each monthly panel define
`R[t] = 1-q[t]/100`, the monthly mean observed positive price ratio. Estimate
only

`E[R[t+h] | R[t]] = exp(a_h + b_h*log(R[t]))`.

Use Poisson pseudo-maximum likelihood for this **continuous positive response**
as a conditional-mean specification; do not assert that ratios are counts or
have Poisson variance. The mathematical form is nonlinear in the original
discount. It is a method repair/challenger, not fulfillment of an exclusively
linear-in-discount specification or a test of control, liquidity or payout
causality. The mean-model rationale is documented in
[Gourieroux, Monfort and Trognon's original working paper](https://www.cepremap.fr/depot/couv_orange/co8203.pdf)
and the [authors' Log of Gravity methods page](https://personal.lse.ac.uk/tenreyro/LGW.html).
Those are estimation references, not empirical evidence for LOOP correction.

Do not fit log terminal ratios by OLS and simply exponentiate: the result need
not be the arithmetic conditional mean ratio, creating a retransformation
mismatch with discount-change MSE. An exponential conditional **mean** link
instead gives the candidate discount forecast
`qhat[t+h]=100*(1-Rhat[t+h])`; score `qhat[t+h]-q[t]` on the original scale.

**Three predeclared benchmarks, on exactly the same matured training rows j:**

1. Persistence: `Δqhat=0`.
2. Mean change: `Δqhat=mean(q[j+h]-q[j])`.
3. Terminal-level mean: `Δqhat=mean(q[j+h])-q[t]`.

The intercept-only positive mean fit is exactly the third benchmark after the
affine ratio/discount transformation. It does not assume that zero discount
is fair value. Keep the existing LH-LEVEL OLS and fixed lambda=1 ridge forecasts
as frozen challengers, also scored against all three benchmarks. This is one
registered comparison, not a penalty, feature, transformation or window grid.

**Samples, timing and estimands.** Use the original LH-LEVEL expanding training
policy, all eleven evaluable comparisons, both frozen coverage rules and exact
24/60/120-month endpoints. Features, scaling and fitting use only matured labels
available at each original origin. Preserve the original minimum of 36 usable
training rows and ten rows per parameter. Use identical origins across the
comparisons; retain solver failures explicitly rather than silently presenting
an easier subset. Do not extend older prices or add annual facts. Ten-year
forecast evaluation stays blocked where the original sample has no eligible
origins. Report squared-error loss differences in original discount percentage
points, RMSE, all nonoverlap phases and fixed calendar-period results. Do not
replace MSE with quasi-deviance after seeing the answer.

**Go/no-go.** Arithmetic, chronology, source hashes, finite fits, positive finite
ratios and terminal `qhat<100` are mandatory implementation gates. Underflow,
overflow or nonconvergence is a recorded failure, not a reason to clip output,
bound b after inspecting results, delete an origin, or try alternative solvers
until a favorable result appears. Independent reconstruction must pass before
reporting model losses.

Passing support by construction is **not** evidence of predictive skill. A
persistence/mean-change win without a terminal-anchor win supports at most
scoped correction toward an anchor; do not claim incremental conditional-state
information. An exposed-history win over all three is a candidate for the
prospective registry, not permission to select it for deployment. If the method
loses, preserve the failure rather than searching another link or window.

## Experiment 2 — A narrow Novo measurement and prehistory request

**Tree:** M01–M05, X01–X03, B02, P01/P03. **Economic hypothesis:** a persistent
class/receipt segmentation state predicts future discount correction. **Rivals:**
asynchronous prices/FX, quote-source substitution, historical ratio/nominal-unit
changes, company transitions and dividend/ex-date timing create the apparent
state. Cash deductions may matter to a trade's payoff without explaining the
observed price-gap predictor.

**Acquisition scope.** Start with the exact Copenhagen B and NYSE NVO instruments,
not another issuer, OTC receipt, Nasdaq predecessor or generic annual ownership
panel. Ask for historical **quote-source venue provenance**, stable identifier
intervals, price-status definitions, currency/quote units and dated receipt/local
share basis for the already exported **1995–2004** candidate interval. Retain
the 2000 demerger and 2001 nominal-share/receipt-basis transition as separate
interval gates; do not assume a stable vendor key proves unchanged economics.
The existing raw data need not be reacquired if the requested provenance can
be supplied and linked to those exact records. A present-day exchange code or
another CSV without historical source venue does not close the gate.

Separately request an explicitly bounded **synchronized-quote feasibility
pilot**, before any large intraday acquisition: the first five common trading
days in each of December 2007, March 2014, November 2023 and March 2025. Dates
are fixed calendar probes across known basis regimes, not selected by large
discounts or forecast errors. Obtain the official Copenhagen closing-auction
event/publication timestamp, the exact NYSE receipt bid/ask no later than that
event, and contemporaneous FX with source/time conventions. Determine the
historical UTC/DST rules. Fix a maximum quote age, such as 60 seconds, before
reading the pilot values; missing or older quotes remain unusable. Do not
silently substitute the later NYSE daily close or a same-date reference FX.
The pilot diagnoses feasibility and measurement differences; twenty dates
cannot certify a multi-decade synchronized panel or establish forecast skill.

**Estimands.** For the pilot compare same-event-time local-equivalent/receipt
ratios with the existing asynchronous daily definition on matched dates. Keep
bid/ask intervals and the FX basis visible. For 1995–2004, produce explicit
released/held security-date intervals and actual positive-price coverage,
including missing/status and split-clock exclusions. Only after the gate passes
may a new frozen historical specification test whether genuinely longer history
changes the 24/60/120-month loss comparisons. Determine actual matured-label
and nonoverlap counts; do not promise ten-year validation from an export start.

**Go/no-go.** Release an old interval only with linked historical source venue,
identity, units/currency, status, ratio/split and continuity evidence. If those
cannot be obtained through an entitled or public route, keep it held and
continue Experiment 1/current samples. If synchronized quotes are unavailable,
mark the timing hypothesis unresolved; absence is not evidence against it.
Material clock/basis discrepancies trigger a new measurement version before
an economic interpretation, not a convenient subtraction or post-loss filter.
Full cash-return testing additionally needs actual distributions/withholding/
fees and execution/funding; that is distinct from predicting the specified
observed discount. More fee facts should not block unrelated price work.

## Experiment 3 — Prospective actual-delivery registry

**Tree:** B01/B02, M01–M03 and the source-specific X/P branches above.
**Hypothesis:** the frozen state relationship survives new economic periods
and the information actually delivered by the forecast origin. **Rivals:**
historical-vintage availability, dependence, adaptive selection and transient
measurement regimes account for the retrospective gains.

Before opening new outcomes, freeze the eligible **active exact-security**
roster, models, benchmarks, monthly construction, delivery-age rule, label
definition, refit schedule and evaluation plan. Do not issue new historical
Shell A/B or retired Roche Genussschein forecasts, or splice them to successor
classes. A new successor class needs its own qualification and training history.
The original price-only linear baseline and fixed ridge should remain visible
alongside the single positive-mean challenger, irrespective of which looks best
in Experiment 1. This prevents a retrospective winner from silently becoming
the sole prospective candidate.

Use the first entirely post-registration completed calendar month as the first
feature cohort—normally December 2026 if registration occurs in November 2026.
Issue only after that month's qualified data are actually received. Log the
receipt and issuance timestamps, immutable raw/as-of hashes, available features,
training-label ends, fitted parameters, all candidate/benchmark predictions,
target month and missing/failure reasons. Establish a source-specific maximum
delivery age from the authorized feed's documented latency before issuance;
do not infer a first-of-month availability clock. Retain both nominal feature-
to-target calendar horizon and actual issuance-to-target lead time.

Register twelve consecutive monthly origin cohorts first, with **24 months
primary** and 60/120 months secondary. Refit only on labels matured and available
by that issuance time; predictions and benchmarks are locked before targets.
No interim loss-driven refit-policy, feature, model, penalty, roster or stopping
change. New sources or genuine class transitions use a separately versioned
protocol. A manual/as-authorized ingestion workflow is sufficient; no cron,
unattended transfer, external account access or deployment is implied here.

**Go/no-go.** Missing delivery/identity/basis gates mean no forecast, explicitly
recorded; forecasts cannot be reconstructed after targets are known. Any
chronology or hash failure blocks that issuance path. At maturity compare
paired original-scale MSE against all three baselines on the frozen common
origins and report native coverage too. A lower historical or prospective point
estimate alone is not a validation label; materiality and uncertainty must be
assessed with dependence and regime stability explicit. A twelve-month origin
cohort is not twelve independent two-year outcomes. More independent periods
or a justified cross-security design are needed before claiming stable skill.

If the first feature month is December 2026, its 24-month target completes in
December 2028, its 60-month target in December 2031 and its 120-month target in
December 2036. The twelve-cohort target windows then extend through November
2029/2032/2037, respectively. No amount of historical recycling creates this
prospective evidence sooner.

## What should not divert this program

Berkshire's one-way conversion/execution study is a credible **separate
short-horizon implementation branch**, with its own financing and executable-
fill gates. It does not advance the primary 24/60/120-month discount-change
question merely because its gross diagnostic Sharpe is high. Do not launch
new daily strategies, threshold optimization, broad factor searches or a
universal liquidity model under this long-horizon batch.

Likewise, the annual structural evidence is valuable but remains gated by
definitions, class/aggregate denominators, nominal/split-restated units,
proposal/interim/final status, source revisions and release timing. Qualify a
specific causal rival and a small admissible feature history before fitting a
structural extension. More historical rows without these distinctions are not
the scientific bottleneck now.

## Post-test adjudication — verified LH5 result

Added **2026-11-12 21:49 UTC**, after the original recommendation above and
after the coordinating agent completed the registered experiment. This addendum
does not rewrite the pre-estimation hypotheses, benchmarks or go/no-go rules.
Sources: `runs/loop_long_horizon/v5_15309415/scores.csv`, `summary.json` and
`verification/AUDIT.json`. Main job `15309415`; separate arithmetic verification
`15309602` passed. All 5,026 quasi-mean forecasts were reconstructed, with maximum
difference 8.60e-11 discount percentage points; 5,514 score/phase/period rows,
the identical matured-row benchmarks, positive support, complete origin
accounting and preservation of prior inputs/outputs passed. This is an
arithmetic/source check, not a new independent economic sample.

**Novo's additional fitted state dependence did not beat the terminal anchor.**
OLS, fixed ridge and the positive-mean candidate all lose to the terminal-level
training mean at both horizons and under both coverage rules, while retaining
their gains against persistence and mean change:

| Novo coverage | Horizon | Forecast origins | PPML R² vs persistence | OLS R² vs terminal mean | Ridge R² vs terminal mean | PPML R² vs terminal mean |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| Pragmatic | 24 months | 176 | 0.404268 | −0.011379 | −0.173817 | −0.011480 |
| Strict | 24 months | 154 | 0.402089 | −0.015441 | −0.163943 | −0.015572 |
| Pragmatic | 60 months | 105 | 0.162290 | −0.030329 | −0.014376 | −0.030301 |
| Strict | 60 months | 93 | 0.157528 | −0.019484 | −0.013286 | −0.019446 |

The support repair worked on all original eligible origins without a solver
failure. That satisfies its necessary implementation gate. It does not add
economic information or establish a superior forecast. Do not try another link,
penalty, window or newly winning stock to avoid this outcome.

### What this does and does not imply

The terminal anchor predicts `Δq=estimated_terminal_center-q[t]`. It therefore
**uses the current discount to predict its subsequent change**, even though
its forecast terminal level does not vary conditionally with the current state.
Beating persistence with that rule can satisfy the original discount-change
forecasting objective. Failure to beat it does not erase the original losses
and gains, prove no predictability, or prove that the measured relationship is
an artifact. The new comparison instead fails to establish incremental MSE value
from the models' extra fitted conditional-state relationship on exposed history.

A simple illustration explains why the distinction matters. Suppose the gap is
`q[t]=mu+epsilon[t]`, with a stable center mu and independent zero-mean disturbances
of variance sigma². If mu were known, persistence's change-forecast MSE would
be `2*sigma²`, while the anchor `mu-q[t]` would leave MSE `sigma²`: R² versus
persistence would be 0.5 despite **no changing conditional terminal mean**.
This is an analytical example, not an estimated explanation for Novo. The
disturbances could be real transitory relative-price movements, quote/FX timing
noise, or both. Estimated-center uncertainty, serial dependence, structural
change and overlapping outcomes complicate the actual sample.

The scientifically sharper next question is consequently: **is Novo's
source-defined terminal-gap center sufficiently stable and economically
meaningful to forecast future observed changes, or is the apparent anchor
largely measurement-specific or regime-dependent?** That directly connects
B01/B02 with M01–M05 and X01–X03; it does not require a new feature search.

### Consequence for the remaining experiments

Experiment 2 is now the leading substantive investigation. Prioritize exact
source venue, dated nominal/receipt basis and the synchronized-quote pilot.
Preserve segmentation/access/holding-cost changes as rivals to a stable
measurement-defined center. Event-specific cash notices may explain particular
cash or ex-date differences, but cannot by themselves establish that the
multi-year center is structural or date a general fee regime. Do not claim
stationarity from a favored test or choose a break date after seeing losses.

Experiment 3 should explicitly retain a **frozen prospective terminal-anchor
versus persistence contrast**, alongside the already registered mean-change and
model comparisons. Its purpose is to determine whether the simple center-based
change forecast survives actual new delivery vintages and periods, not to
promote the retrospectively best method. Keep all twelve origin cohorts,
original targets, failed/missing issuances and dependence limits. No model is
selected for live use from this exposed-history result.
