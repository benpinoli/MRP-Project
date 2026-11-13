# For Ben: discount research snapshot

**November 12, 2026 · America/Denver**

Start with the seven-slide presentation, then the timeline. The paper explains the evidence in detail; the long table makes the unsuccessful comparisons easy to inspect.

| File | Contents |
| --- | --- |
| [ACCOMPLISHMENTS.pptx](ACCOMPLISHMENTS.pptx) | Short, editable PowerPoint presentation |
| [ACCOMPLISHMENTS.html](ACCOMPLISHMENTS.html) | Same seven slides in an offline browser deck; use arrows or Space, P to print |
| [PRESENTATION_PREVIEW.png](PRESENTATION_PREVIEW.png) | Overview of all slides |
| [PRESENTATION.md](PRESENTATION.md) | Plain-text slide content |
| [LOCAL_AI_REVIEW_PROMPT.md](LOCAL_AI_REVIEW_PROMPT.md) | Independent presentation and table review instructions |
| [TIMELINE.md](TIMELINE.md) | Condensed sequence of questions, tests and findings |
| [PAPER.md](PAPER.md) | Research synthesis, 21 evidence sections and all 44 tree nodes; includes plans and acquisition work as well as empirical tests |
| [HYPOTHESIS_TREE.md](HYPOTHESIS_TREE.md) | Readable tree with mechanisms, rivals, evidence and remaining tests |
| [HYPOTHESIS_TREE.json](HYPOTHESIS_TREE.json) | Unchanged snapshot of the canonical machine-readable tree |
| [WHAT_DID_NOT_WORK.md](WHAT_DID_NOT_WORK.md) | Long table grouped by discount situation and regression variables |
| [WHAT_DID_NOT_WORK.csv](WHAT_DID_NOT_WORK.csv) | Same 543 specification cases for sorting and filtering |

## Does Novo have predictive power?

**Yes: there is historical predictive content in the measured discount against some benchmarks. Future predictive skill is not yet established.**

For example, Novo's rolling120 level OLS reduced historical mean squared forecast error versus predicting no change by **39.55% at two years and 13.59% at five years**, under pragmatic coverage. Against the mean of past discount changes, the reductions were **43.55% and 20.90%**. These are reductions in forecast loss, not investment returns or estimates of statistical significance.

The stronger rival is a simple **training-only mean terminal discount**. It can predict a discount change by subtracting today's discount from that historical center. Thus finding that a conditional model does not beat the center is not finding that the center has no predictive content.

| Novo rolling level OLS, pragmatic coverage | Two years | Five years |
| --- | ---: | ---: |
| MSE reduction versus no change | +39.55% | +13.59% |
| MSE reduction versus mean historical change | +43.55% | +20.90% |
| MSE reduction versus matching terminal mean | −1.57% | −6.47% |

Positive means lower error. Most fitted level/state models add no demonstrated value over the terminal anchor in these comparisons.

There is a **limited additional signal**: the five-year expanding activity OLS model beats its matching anchor by **6.81% pragmatic / 5.11% strict MSE**, on 88/74 overlapping origins. It also beats simpler regressions on those same origins. But the advantage does not survive rolling training or ridge. Nonoverlap phases contain only one or two outcomes, and volume activity is not an observed liquidity cost.

The defensible conclusion is **a historical candidate with strong benchmark dependence**, rather than proven future skill or an executable arbitrage. The history has been viewed, source-vintage/venue/clock/basis qualifications remain, no future forecast has yet been issued, and the synchronized pilot still has all sixty primary slots missing. The candidate FX rows do not close those gaps.

Source: [complete verified comparison](../docs/regressions/LOOP_TREE_PRODUCTIVE_BATCH_RESULTS_20261112.md), [aggregate scorecard](../docs/regressions/LOOP_TREE_PRODUCTIVE_BATCH_SCORES_20261112.csv), [paper T20](PAPER.md#t20-matching-memory-terminal-anchors-across-all-existing-price-designs).

## How to read the failure table

The 543 rows are **dependent specification cases, not 543 independent hypotheses**. Many share observations across horizons, methods, windows and cleaning rules. Each row identifies its regression variables, target horizon, training policy, coverage, sample size and failed comparison. A model may beat persistence yet lose to the terminal mean; both facts remain visible.

Forecast losses, development-gate failures, weak explanatory fits, unrun tests and constant-regressor identification failures are distinguished. The table does not turn missing data into a negative finding or erase the retained successful comparisons.

The daily/US aggregate metrics needed to independently check the table are in [TABLE_INPUTS/SOURCES.json](TABLE_INPUTS/SOURCES.json). The build script can use these copies when private run directories are unavailable.

## Scope and navigation

These are snapshots for review. Original research files remain under [docs/regressions](../docs/regressions/); copying them here did not change estimates or verdicts. Core links inside this folder work directly; detailed evidence links point back into this repository, so keep the folder in the repo to follow them. The presentation and its preview are self-contained and can be shared separately.

Only aggregate documentation and scores are included. No licensed observation rows, private crosswalk records, account captures or credentials are packaged here. [SOURCE_SNAPSHOTS.json](SOURCE_SNAPSHOTS.json) records the source hashes; the validation/manifest files record package checks. No new regression was run to prepare this folder.
