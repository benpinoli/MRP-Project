# Conditional mean versus terminal anchoring: verified result

November 12, 2026. The registered test changes the next scientific priority:
Novo's original persistence and mean-change wins remain, but none of the tested
conditional models improves on the training-only mean terminal discount. A
simple terminal anchor can itself forecast changes. The next question is whether
that center is stable and correctly measured, then whether it predicts new
origins. Further link/window/predictor searching is not the active next step.

## What was agreed and executed

The coordinating and analyst agents first distinguished support-invalid
extrapolation, generic terminal anchoring and incremental conditional-state
information. Before estimation, the [protocol](LOOP_LH5_MEAN_PROTOCOL_20261112.md),
`configs/loop_long_horizon_v5.json`, tree and ledgers registered one positive
conditional mean and the additional terminal-level benchmark. The analyst's
[design and separately dated adjudication](LOOP_NEXT_EXPERIMENT_REVIEW_20261112.md)
preserve the original proposal rather than rewriting it after the result.

For R=1-q/100, estimate `E[R[t+h]|R[t]]=exp(a+b*log(R[t]))` with a continuous-
response Poisson quasi-mean objective, not exponentiated log-OLS or a count
distribution. This is a support/mean-method challenger nonlinear in q; it does
not silently replace the original linear-only specification or establish an
economic mechanism. No alternate links, penalties, windows or predictors were
searched, and no invalid original forecast was clipped or removed.

Main Slurm job `15309415` completed all **5,026 original eligible LH-LEVEL
origins**, across eleven evaluable comparisons, both coverage rules and 24/60-
month horizons. All predicted ratios are positive and finite; no fit failed and
no terminal discount rounded to 100. Short samples and ten-year evaluation
remain blocked as originally recorded. New price intervals and structural
features admitted: zero. Private run: `runs/loop_long_horizon/v5_15309415/`.

Original expanding OLS and fixed-lambda1 ridge were retained. Every method was
scored in the original discount-change percentage-point units against the same
three benchmarks, using identical matured training rows and forecast origins:

1. Predict zero change.
2. Predict the mean matured historical change.
3. Predict the mean matured terminal discount, minus the current discount.

The third is an intercept-only terminal-mean anchor. It is not a full-sample
equilibrium, a forced zero discount or a historical change average. All label
endpoints precede or equal the completed feature month; the latest matured
terminal observation can be the known current month, never a future target.

## Novo's discriminating comparison

R-squared below is relative to the **terminal-level mean benchmark**. Negative
means the fitted model has higher squared forecast loss than that benchmark.

| Horizon | Coverage | Original OLS | Fixed ridge | Positive conditional mean |
| --- | --- | ---: | ---: | ---: |
| 24 months | Pragmatic | -0.01138 | -0.17382 | -0.01148 |
| 24 months | Strict | -0.01544 | -0.16394 | -0.01557 |
| 60 months | Pragmatic | -0.03033 | -0.01438 | -0.03030 |
| 60 months | Strict | -0.01948 | -0.01329 | -0.01945 |

All twelve comparisons lose to the terminal anchor. Against persistence, the
positive-mean candidate still has pragmatic R-squared 0.40427 at two years and
0.16229 at five years; its old-style mean-change comparisons remain positive
too. The original wins are not erased. What is not demonstrated is additional
value from the fitted conditional slope beyond generic terminal anchoring on
these exposed origins. The small point-loss differences do not prove that no
conditional information exists in any population or future regime.

An illustrative model makes the distinction clear. If q[t]=mu+epsilon[t] with
independent, constant-variance noise and known mu, persistence's change error is
epsilon[t+h]-epsilon[t], with MSE 2*sigma². The terminal-anchor change forecast
mu-q[t] leaves error epsilon[t+h], with MSE sigma² and R-squared 0.5 against
persistence. This is a mathematical illustration, not a fitted model or causal
claim about Novo. It can describe a real stable observed gap or transitory
measurement/price noise. The anchor explicitly uses today's q to predict its
change even though the terminal conditional mean is constant.

## Full comparison retained

The [complete scorecard](LOOP_LH5_MEAN_SCORECARD_20261112.csv) contains all 132
method/sample/horizon/coverage scores, with MSE/RMSE/MAE and all three benchmark
losses. No new winning stock is promoted because Novo lost the new comparison.

| Method | Horizon | Persistence wins, pragmatic / strict | Mean-change wins, pragmatic / strict | Terminal-anchor wins, pragmatic / strict |
| --- | --- | --- | --- | --- |
| Original OLS | 24m | 4/11 / 4/11 | 7/11 / 6/11 | 2/11 / 2/11 |
| Positive mean | 24m | 4/11 / 4/11 | 7/11 / 6/11 | 2/11 / 2/11 |
| Fixed ridge | 24m | 6/11 / 6/11 | 10/11 / 10/11 | 6/11 / 6/11 |
| Original OLS | 60m | 4/11 / 4/11 | 6/11 / 6/11 | 4/11 / 4/11 |
| Positive mean | 60m | 4/11 / 4/11 | 6/11 / 6/11 | 4/11 / 4/11 |
| Fixed ridge | 60m | 3/11 / 3/11 | 9/11 / 9/11 | 3/11 / 3/11 |

These are descriptive counts, not independent experiments or significance
tests. All nonempty nonoverlap phases and the previously fixed calendar-period
summaries remain private. Five-year phases still often have one or two outcomes.
The positive-mean method passes the mathematical support gate; that alone is
not predictive improvement, a liquidity/supply mechanism or deployability.

## Verification

Independent Slurm job `15309602` reconstructed all 5,026 quasi-mean predictions
using a full two-parameter Newton mean-score solver, compared with the main
profiled-intercept/slope-bisection solver. Maximum prediction difference was
8.60e-11 percentage points. All **5,514 score/phase/period rows**, three-benchmark
training masks, positive-ratio support and original-origin counts passed.
Original baseline, ridge outputs and source inputs remain hash-identical.
Private receipt: `runs/loop_long_horizon/v5_15309415/verification/AUDIT.json`.
This is independent arithmetic reconstruction, not a separate economic sample
or an independently reproduced historical vendor vintage.

Synthetic checks cover exact power-mean recovery, a constant terminal mean,
arithmetic anchor identity on the original scale, ratio-unit equivariance,
positive support and invalid/constant-input rejection. Executed code/config,
training boundaries, coefficients, forecasts, failures and input/output hashes
are saved privately. No licensed rows or individual forecast origins are public.

## Scientific decision

Close the single method experiment and preserve its answer. Treat stable
terminal anchoring as the simpler active forecasting hypothesis, with economic
integration/segmentation and quote/FX/ratio noise as rivals. Do not relabel this
as proof of pure artifact, rejection of every state model, or removal of the
original goal's observed-discount prediction gains.

Next, execute the [narrow Novo data request](LOOP_NOVO_TARGETED_DATA_REQUEST_20261112.md)
through an entitled/public route and retain unresolved provenance as unresolved.
In parallel, the [prospective registry](LOOP_PROSPECTIVE_REGISTRY_20261112.md)
predeclares a terminal-anchor-versus-persistence primary contrast and retains
all frozen candidates and benchmarks. No future forecast is issued yet.
The [active plan](LOOP_ACTIVE_RESEARCH_PLAN_20261112.md) is the operational queue;
Berkshire execution, broad annual acquisition and new model grids do not divert
this long-horizon program.
