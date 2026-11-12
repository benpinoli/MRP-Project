# LOOP discount prediction over two to ten years

The objective is a small linear model for future changes in observed relative-price
discounts at 24, 60 and 120 calendar months. This extends the existing structural
hypothesis tree across LOOP stocks while preserving earlier Samsung and daily
results. A class-price discount is distinct from a required return or valuation
discount rate; this batch estimates the former. The November 12 user instruction
authorizes this new scope; old paused agents/jobs are not restarted.

## Hypotheses and frozen models

B01/B02 motivate the question whether current discount states contain useful
long-run correction information beyond persistence. L01 asks whether relative
trading activity adds information; it is a quantity proxy, not measured liquidity
cost. M01/M02 govern cleaning and share bases. Three nested intercept models
predict `q[t+h]-q[t]`: current discount; discount plus trailing twelve-month
change; and those two variables plus relative activity. Compare activity with
the middle model on identical origins. There is no feature search or tuning on
test losses. Supply, ownership, control, payout, cash rights and funding remain
distinct mechanisms; missing histories are not zeros or rejected hypotheses.

## Measurement and pragmatic samples

Start from the verified private daily candidate membership. Exclude isolated
stale, missing or unmapped records without blocking the issuer. No future-price
backfill or interpolation is used. Preserve asynchronous split windows and keep
Shell A/B/unified and Roche Genussschein/participation samples separate.

For common/preferred, use `q=100*(1-P_preferred/P_common)`; for Roche compare
nonvoting with voting. For A/H convert H to CNY and compare with A. For local/ADS,
use `q=100*(1-ratio*local_in_USD/ADS)`, positive when the local equivalent is
cheaper. Zero is not universally fair value across different legal rights.

Average daily ratios within months, not separately averaged leg prices. Main
months need ten observations and 50% coverage of supplied weekday grid rows;
the frozen strict sensitivity needs 80%. This is an observed-date proxy, not a
certified exchange calendar. Keep unqualified/empty months on the calendar grid.
Exclude partial November 2026; local series end October and CRSP series September.

Observed daily ECB references, in foreign units per EUR, give exact-date
cross-rates without extrapolation. Preserve URL, retrieval time and file hash.
Asynchronous closes and current historical FX vintages define retrospective
monthly gaps, not executable parity. ADS ratios use the delivered matched-basis
assumptions with historical-certification limits explicit. Shell's GBP scale
uses the earlier magnitude evidence; it remains an assumption pending independent
quote reconciliation. These limitations qualify cross-market findings without
blocking unrelated same-currency models.

## Predictive evaluation

Features are completed monthly means, nominally available on the first day of
the next month. Original delivery vintages are unavailable: evaluation is
retrospective pseudo-out-of-sample on exposed history. A future production claim
requires a new prospective cohort and verified publication/delivery timing.

At each origin, use only earlier-origin training rows whose h-month outcomes
have ended by the completed feature month. Require 36 usable rows and ten rows
per coefficient, including intercept. Fit/scaling use only training rows.
Compare identical origins against zero change and the training mean change;
compare nested models on common origins. Exact calendar endpoints prevent a
missing month from shortening a horizon. No daily return is formed by lagging
the filtered membership file.

Full-sample coefficients and HAC(h) errors are exploratory, not confirmatory
inference. Record anchored nonoverlapping outcomes and forecast counts. Roughly
twenty years may provide no feasible ten-year train/evaluation split under the
declared minimum: this is insufficient evaluation history, not a null finding.
Future full-fit projections remain unvalidated conditional candidates. See
[long-horizon inference](https://www.federalreserve.gov/pubs/feds/2009/200927/index.html)
and [out-of-sample benchmarks](https://www.nber.org/papers/w11468).

## Checkpoints and evidence

The frozen executable configuration is `configs/loop_long_horizon_v1.json`.
Unique ignored run directories retain input/code/config hashes, monthly panels,
coefficients, forecast/training boundaries, failures, coverage, comparisons and
conditional future projections. Per-class checkpoints and an atomic progress
file preserve completed work. Failed runs remain; retries require diagnosis.

Update the canonical JSON tree, readable tree, execution ledger and evidence
ledger before/after each batch. Preserve historical IDs and distinguish supported
arithmetic, model-specific rejection, promising association, missing evidence and
validated prediction. Public Git contains code and aggregate research only.
