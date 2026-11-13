# Conditional information versus a terminal anchor

Registered before new estimates on November 12, 2026. This experiment follows
discussion with the analyst and the B01/B02/M01/M02 branches of the hypothesis
tree. The original linear models, specifications, sources and results remain
unchanged. The versioned configuration is `configs/loop_long_horizon_v5.json`;
outputs remain in a new ignored `runs/loop_long_horizon/v5_JOBID/` directory.

The goal is still prediction of 24/60/120-month changes in observed monthly
class-price discounts. This experiment is a limited statistical falsification,
not a new economic explanation. It asks whether the current state contains
information beyond an unconditional terminal-level anchor. It also fixes the
mean model's support definition without clipping the failed linear forecasts.

Set R=1-q/100, which is positive under the existing monthly price-ratio
definition. Fit exactly one conditional mean:

`E[R[t+h] | R[t]] = exp(a_h + b_h * log(R[t]))`.

Use the Poisson quasi-mean objective on continuous positive ratios; this is not
a count distribution, and no Poisson variance inference is claimed. Profile
the intercept and solve the convex mean score. A log-OLS regression followed
by exponentiation would target a different geometric quantity and is not an
allowed substitute. This model is nonlinear in q and is a diagnostic comparator,
not a silent relaxation of the original linear-only specification.

Use only the original LH-LEVEL eligible forecast origins and exact expanding
matured-label training rows. Preserve calendar endpoints and missing months,
pragmatic/strict coverage, the 36-row/ten-per-parameter minimum, source hashes
and all venue, identity, unit, ratio, split and corporate-transition exclusions.
No new interval or structural feature is admitted. Retain all blocked baseline
rows, including short panels and ten-year evaluation. Failed numerical fits
remain explicit; missing forecasts are not counted as wins.

Score the predicted change `100*(R[t]-predicted_R[t+h])` in the original q-change
MSE/MAE units. On identical origins compare the new model and saved original
OLS/fixed-lambda1 ridge with three training-only benchmarks:

1. Zero change.
2. Mean matured historical change, as before.
3. Mean matured terminal q[j+h], minus the current q[t].

The third benchmark does not impose a zero terminal discount or an economic
equilibrium. It uses the exact same matured rows as the state model and can
change with each expanding training vintage. The intercept-only quasi-mean
ratio fit gives this same terminal anchor after the affine conversion to q.
Registering it before fitting separates state-dependent information from simple
anchoring, particularly when a discount-change slope is close to minus one.

Keep both original comparators and every outcome. No alternative link, penalty,
slope constraint, window or predictor is selected after observing losses. Save
positive-ratio support and numerical checks, training boundaries, coefficients,
failures, all nonempty nonoverlap phases, scores against every benchmark,
executed code/config and input/output hashes. Independently reconstruct the fit
with a two-parameter mean-score solver and verify scoring arithmetic.
Retain the previously fixed through-2014, 2015–2019 and 2020-onward origin-year
groups as descriptive checks; do not choose new breaks from these results.

Arithmetic/support success is mandatory. Predictive comparisons remain exposed-
history diagnostics. If Novo does not beat the terminal anchor, do not label
its persistence/mean-change wins evidence of extra conditional-state information.
If it does beat all three benchmarks under both horizons and coverage rules,
retain a candidate for measurement and prospective testing; do not claim a
validated model. Phase outcomes are not independent replications. A numerical
repair or more favorable loss does not identify fees, ownership, liquidity or
economic convergence as the cause.
