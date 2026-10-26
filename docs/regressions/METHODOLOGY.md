# RG estimation methodology 1.0.0

Author: Codex, 2026-10-26. Every current model is exploratory and specified before its first regression run; the descriptive history has already been viewed. Configured dates are fixed before estimation. [Configuration](../../configs/samsung_regressions.json) is canonical for executable model columns, windows and HAC lags; this file defines their interpretation.

## Outcomes and units

For synchronized comparable raw common and preferred prices C and P, d=1-P/C, q=100d and g=log(C/P)=-log(1-d). Primary `dd_pp` = q_t-q_(t-1); positive means widening. Secondary `dg` = g_t-g_(t-1), dimensionless. Example: C=100, P rises from 80 to 82 with common unchanged: discount falls 20%→18%, `dd_pp`=-2 and `dg`=log(80/82). A simultaneous equal split cancels in the price ratio; unequal class actions require an entitlement audit. Neither outcome is a dividend-adjusted return.

Retain each observed session in the existing EP01 grid, including ineligible pairs. Difference and lag BEFORE complete-case filtering. Mask both affected change endpoints when sensitivity removes a date; never difference across a removed date. Dates absent both classes remain a calendar limitation. Long intervals and other review flags remain visible in main and masked in sensitivity. No winsorization, interpolation or zero replacement.

## Model families

Baseline B00: `dd_pp_t = alpha + rho*q_(t-1) + e_t`. B01: `dd_pp_t = alpha + beta'F_t + e_t`. B02 uses `dg_t`. B03 adds lagged q to B01. B04 adds lagged log(preferred/common volume) as an activity control, not an observed trading cost. These nested comparisons must also be refit on a common complete-case sample before incremental fit is interpreted; the initial engine reports native samples and marks this follow-up required.

Mechanism models use `dd_pp_t = alpha + beta'F_t + rho*q_(t-1) + gamma'Z_(t-1) + e_t`. All optional columns are defined in [FACTORS.md](FACTORS.md). J01 includes all named mechanism columns together; X01/X02 add explicitly registered products. A lag establishes ordering under the declared availability rule, not exogeneity. Contemporaneous F is an explanatory control; these models are not forecasts. Coefficients remain in original units; include intercept; solve with least squares, no unannounced selection.

## Barra and residual interpretation

Prefer Korea-model or verified Korea-covered global factors with documented return currency. A US model can measure external state but cannot be labeled Korean specific risk. The shipped API is [load_factors](../../src/sf_quant/data/factors.py); static names are [here](../../src/sf_quant/data/_factors.py). Select a modest core (market, value, size, momentum, liquidity, volatility, leverage, yield, profitability/growth where actually available) plus semiconductor exposure, then a broad-factor sensitivity after rank checks. The default executable config uses shipped US names and therefore requires explicit US-sensitivity acknowledgement in metadata. Replace names after inspecting the actual Korea/global export; never invent a Korean prefix.

For verified class total returns r_j,t, attribution would be `r_j,t=b_j,t-1' f_t + u_j,t`, then `r_C-r_P=(b_C-b_P)'f+(u_C-u_P)`. This vendor-exposure method requires dated exposure identifiers, return conventions and lagged exposures. A time-series fit of `dg` on F instead estimates constant statistical loadings of a relative price change. Its residual is a model-conditional gap innovation, not a vendor specific return. Returns and factor-adjusted price changes also mix cash-flow and required-return news; identifying a discount-rate change needs additional valuation restrictions. The current engine implements the latter gap regressions only.

Use a joint regression to estimate mechanism coefficients conditional on F. If using Frisch–Waugh–Lovell for interpretation, project BOTH y and Z off exactly the same intercept/F matrix on exactly the same rows; residualizing only y is wrong. Retain joint-regression inference. Full-sample residuals must not be used in predictive evaluation; rolling/expanding nuisance fits must be estimated solely on the training past.

## Timing and holidays

Every Korean endpoint has an explicit UTC close from `sessions.csv`. Factor rows have observation date, actual return-period end UTC and availability UTC from `factor_timing.csv`. For the explanatory default, sum arithmetic factor returns whose period END falls in `(previous_Korean_close, current_Korean_close]`, requiring every included row to have been available by the current endpoint. The supplied factor trading calendar must declare every expected observation; absent observations fail preparation. Multiple foreign sessions during a Korean holiday are summed. Empty bins are missing, never zero or carried. The sum is a factor shock proxy, not compounded investable wealth. Source periods may overlap the Korean interval; end-time binning does not establish synchronized attribution. Save every factor date/bin mapping and interval duration.

For US factors this generally associates the US close of the previous US business day with the next Korean endpoint. No `shift(-1)` or blind calendar-day subtraction. For prediction, aggregate only factors available before the forecast origin; that is a separate, unimplemented design. Revisions and public release timing of optional mechanisms must be addressed in their metadata; a modern restatement is retrospective only.

## Collinearity, inference and sample discipline

Barra factors are not guaranteed orthogonal in a time series; country/industry constraints, extra market proxies, interaction terms and duplicated macro series can introduce dependencies. Check variance, singular values, rank, standardized condition number and VIF. Rank deficiency and standardized condition number >1e8 block fitting; report VIF >10 and correlations rather than silently remove columns. Scaling is for diagnostics only. QR/PCA/ridge may support later predictive sensitivities but change coefficient interpretation and require chronological tuning. Twenty years allow many columns algebraically, but persistence, regime changes and repeated slow data limit effective information. Require n>=max(252,20*k), with k including intercept, and report calendar span and n/k.

OLS covariance uses Bartlett Newey–West scores on the ORIGINAL session grid with missing-row scores set to zero; bandwidths 5, 20, 60 sessions, finite-sample multiplier n/(n-k). Grid holes are not compressed for HAC lag distances. Report asymptotic normal p-values and 95% intervals; these are approximate for persistent lagged-level regressions and sparse events. Export residuals, fitted values, matrix rank, singular values, condition number, VIF and residual lag-1 correlation using adjacent original-grid pairs. Collection applies Benjamini–Hochberg across all successful non-intercept tests in that submission; dependent tests and alternative HAC bandwidths remain exploratory, not confirmatory discoveries.

Full 2005–2026 and fixed 2005–2014 / 2015–2019 / 2020–2026 windows expose stability. A short post-reversal window must not be picked to maximize significance. Low-frequency ownership/policy analyses must count independent releases/events and ultimately use monthly/event inference. Before interpreting persistent levels, run ADF/KPSS with trend/lag sensitivity, inspect structural breaks and verify cointegration for any ECM. A statistically nonzero rho is not alone proof of stable mean reversion. Static levels OLS and causal event claims are outside the initial executable models.

## Follow-up methods and acceptance

After the initial fit: identical-sample nested tests and partial R²; weekly/monthly reaggregation respecting endpoint availability; trailing 756-session beta stability with sufficient n/k; residual autocorrelation/stress diagnostics; contiguous-block bootstrap (20/60-session blocks, recorded seeds) for generated residuals and interactions; dated governance/index/supply events with confound review and lead windows. These are specified follow-ups, not implemented or already run.

Predictive evaluation, if later authorized, uses expanding chronological training, all tuning within training folds, a final untouched calendar holdout, overlap-aware purging, and comparisons against zero change / AR benchmarks. Full-sample explanatory R² is not forecasting evidence. Slow fundamentals use first public release dates and revision vintages, never future accounting period values.

An empirical report is reviewable only with input/code/config hashes, timing/coverage report, exclusions, coefficient uncertainty, unestimated-model reasons, sample definitions, units, and an interpretation against competing mechanisms. Publish no vote value, discount-rate effect or causality from association alone.
