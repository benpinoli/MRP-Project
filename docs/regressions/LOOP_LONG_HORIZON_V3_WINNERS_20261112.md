# LOOP forecast winners against persistence and rolling historical mean

November 12, 2026. These tables cover the verified **v3 rolling-window results**:
OLS and fixed-penalty ridge models trained on eligible origins within the prior
120 calendar months. They do not include the expanding-window results.

**Novo is the only comparison that beats both benchmarks across every tested
model, method, horizon, and coverage rule in these rolling-window results.**

## Definitions

A **win** means lower forecast mean squared error on the same evaluation origins,
equivalently positive out-of-sample R-squared against the specified benchmark.
The target is the change in the observed monthly class-price discount over two
or five years, not a required return or cash-inclusive trading payoff.

- **Zero-change persistence:** predict no change in the discount.
- **Rolling historical mean:** predict the average matured horizon-specific
  discount change in that model's rolling training set. This is not the average
  historical price or discount level.
- **OLS:** ordinary least squares.
- **Ridge:** the prespecified lambda=1 penalty, using training-only scaling and
  an unpenalized intercept; the penalty was not selected from evaluation losses.

Model key:

- **L:** current discount only, plus intercept (`LH-LEVEL`).
- **S:** current discount plus trailing 12-month discount change, plus intercept
  (`LH-STATE`).
- **A:** state model plus relative trading activity, plus intercept
  (`LH-ACTIVITY`).

Unmarked entries win under **both pragmatic and strict coverage**. **(p)** means
pragmatic only; **(s)** means strict only. Pragmatic monthly coverage requires at
least ten observations and 50% of supplied weekday rows; strict requires at least
ten observations and 80%. **—** means none of the listed models wins against
that benchmark in that method/horizon cell. Each comparison is evaluated
separately; the tables do not select a best model for deployment.

## Wins over zero-change persistence

| Stock/class comparison | 2-year OLS | 2-year ridge | 5-year OLS | 5-year ridge |
| --- | --- | --- | --- | --- |
| BYD A/H | — | L, S, A | L, S, A(p) | L, S |
| HDFC local/ADS | — | S(p) | L | — |
| Hyundai common/preferred 1 | — | — | — | S, A |
| Hyundai common/preferred 2 | — | — | — | S, A |
| Hyundai common/preferred 3 | — | — | — | L, S, A |
| **Novo local/ADS** | **L, S, A** | **L, S, A** | **L, S, A** | **L, S, A** |
| Ping An A/H | — | A(s) | — | L(s), S, A |
| Roche voting/Genussschein | — | L, S, A | — | — |
| Historical Shell A | L, S, A | L, S, A | — | — |
| Historical Shell B | L, S | L, S | L, S, A | L, S, A |
| Volkswagen ordinary/preferred | — | — | — | — |

## Wins over the rolling historical mean

| Stock/class comparison | 2-year OLS | 2-year ridge | 5-year OLS | 5-year ridge |
| --- | --- | --- | --- | --- |
| BYD A/H | L(p) | L, S, A | L, S, A(p) | L, S, A(p) |
| HDFC local/ADS | — | L, S, A | L, S, A | L, S, A |
| Hyundai common/preferred 1 | L | L, S, A | L, S, A | L, S, A |
| Hyundai common/preferred 2 | L | L, S, A | L, S, A | L, S, A |
| Hyundai common/preferred 3 | — | L | A | L, S, A |
| **Novo local/ADS** | **L, S, A** | **L, S, A** | **L, S, A** | **L, S, A** |
| Ping An A/H | L | L, S(p), A(p) | — | — |
| Roche voting/Genussschein | — | L, S, A | L, S, A | L, S, A |
| Historical Shell A | L, S, A | L, S, A | — | — |
| Historical Shell B | L, S, A | L, S, A | L, S, A | L, S, A |
| Volkswagen ordinary/preferred | — | S, A | L, S, A | L, S, A |

## Interpretation and exclusions

- BYD's strict five-year activity specification is **not estimable**, so its
  A(p) entries do not represent a strict-coverage loss.
- Shell A/B are retired historical classes, not the current unified Shell
  security.
- Alibaba, unified Shell, and Roche participation lack eligible forecast
  evaluations in this batch; they are not counted as losses.
- There are no ten-year evaluation winners. The baseline lacks sufficient
  matured-label evaluation history, and this fixed training-memory sensitivity
  cannot supply the required ten-year training-label count.
- Monthly forecast outcomes overlap. Five-year nonoverlapping phases often
  contain only one or two outcomes. These are retrospective loss comparisons,
  not statistically established or prospective wins.
- Beating the historical mean does not imply beating persistence. Volkswagen,
  for example, has historical-mean wins while none of these rolling models beats
  persistence.
- No older paired interval or structural predictor was admitted in v3. Historical
  venue, identity, units, split/ratio clocks, publication dates and documented
  exclusions remain binding. Baseline and v2 results are preserved.

## Sources

These tables use rows with `window=rolling120` in the verified aggregate
[v3 scorecard](LOOP_LONG_HORIZON_V3_SCORECARD_20261112.csv). Winners have
`r2_vs_persistence > 0` or `r2_vs_training_mean > 0`, respectively; coverage
markers distinguish the `pragmatic` and `strict` variants.

The [v3 results report](LOOP_LONG_HORIZON_V3_RESULTS_20261112.md) records the
source gates and findings; the [v3 protocol](LOOP_LONG_HORIZON_V3_PROTOCOL_20261112.md)
defines the frozen experiment. Main Slurm job: `15308280`; independent arithmetic
verification job: `15308326`. Public content is aggregate research only;
licensed rows and individual forecast origins remain outside Git.
