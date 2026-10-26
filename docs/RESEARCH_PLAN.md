# Samsung common and preferred research plan

## Active scope — 2026-10-26

The user has authorized regression planning and cluster infrastructure. Start at the [central regression hub](regressions/README.md), which supersedes the earlier descriptive-only stopping instructions below. The new stage includes discount-change models, Barra controls, literature replications/adaptations and economic mechanism extensions. Code and Slurm jobs are prepared; empirical fitting awaits SSH and verified cluster inputs. Historical milestones and archived outputs remain unchanged.

## Current completed milestone

Methodology 3.0.1: [EP01 descriptive figure pack](../runs/samsung/EP01_descriptive/20261022T070701_403388Z/README.md).
All six requested graphs have main and flag-exclusion versions; local flagged
episodes inspected. Thirteen calculation/integrity checks passed; saved-output
arithmetic, hashes and navigation links independently verified. Raw files remain
unchanged. [Research log](RESEARCH_LOG.md) and [hypothesis tree](HYPOTHESES.md)
link every figure and table; all manifests/support files are cataloged in
`research/artifacts.json`. New runs use pair/experiment/UTC folders; older runs
are indexed in place to preserve links. The initial EP01 episode-gap display
was corrected in a fresh run and explicitly superseded in the review log.

Next: independent quote/calendar checks on flagged episodes, followed by the
user's selected descriptive overlay when its inputs arrive. No factor models,
returns or backtests. Earlier scope/plan entries below are historical.

## Current rerun plan 2026-10-22

Specification 2.0.0 supersedes the v1 scope/assumptions below: validate the new
immutable export through October 20, 2026; incorporate supplied vendor field
definitions; treat volume as an audit flag rather than an eligibility gate;
regenerate only the raw-price discount chart. Keep the adjustment formula and
split-adjusted panel deferred. Preserve old raw bytes, runs and observations.

Dependency order: register new input/hash and vendor definitions; version
methodology and test deferral/status behavior; compare overlapping histories;
run raw-price audit/chart; visually inspect; append run findings and remaining
flags. Factor loader documentation is reviewed for future regression planning
only. The user confirms Barra access; no prediction, regression or backtest
is executed at this stage. Future specifications must distinguish the discount
level from discount changes and return outcomes, verify factor geography/units
and Korean-close timing, and audit the existing helper's forward shift.

Scope updated 2026-10-22. The current instruction limits work to E01 raw-price
discount and split-adjusted indexed prices, plus their validation. No prediction,
backtest, valuation overlay, liquidity experiment, or total-return wealth experiment
is authorized in this milestone.

## Repository audit and dependency order

The repository contains the `sf-quant` Python library, `pyproject.toml`, and
`uv.lock`; its market-data loaders are not a WRDS Global CSV ingestion pipeline.
No AGENTS.md was found in the workspace or its checked ancestor directories.
The project brief is the research specification. Existing user deletions and
unrelated untracked documents must remain untouched.

1. Protect the immutable WRDS export and all local run outputs with `.gitignore`.
   Record SHA-256 before and after analysis; verify the raw path is untracked and
   ignored. Do not publish licensed data or derived outputs.
2. Audit every issue in the export, then select Samsung local preferred/common by
   gvkey, iid, ISIN, currency, exchange and issue type. Obtain issuer identity and
   split evidence. Resolve field definitions where publicly accessible; record
   vendor-documentation gaps without pretending they were verified.
3. Implement a small standalone research module under `src/samsung_research`.
   Read raw CSV strings without altering source bytes. Reject duplicate keys and
   identity changes; flag missing, nonfinite, nonpositive, carried, nontrading and
   questionable range records. No automatic price filling or winsorization.
4. Register formulas, filters, figures and decisions in schema-validated JSON;
   generate the corresponding methodology Markdown from that registry. Test
   arithmetic, split continuity, class joins, exclusions and documentation parity.
5. Run E01 from the configured local file. Save normalized audit/paired tables,
   field coverage, report, PNG/SVG figures, source/methodology/config snapshots,
   environment and input/code hashes in a unique immutable `runs/` directory.
6. Visually inspect both figures; record descriptive observations, competing
   explanations, unresolved validation needs, and the next action. Stop here.

## Acceptance and limitations

One documented command regenerates E01 from local data without vendor credentials.
Both figures use exactly matched valid observations and a shared initial index
date. All excluded vendor dates remain gaps. Raw bytes remain unchanged. The run
must record unavailable independent calendar/price reconciliation and inaccessible
WRDS dictionaries as limitations, rather than claiming complete validation.
The filename is not evidence of coverage through 2026.

Commands and the completed run reference are recorded below after execution.

## Session completion 2026-10-22

Implemented and executed the requested E01 subset. Final run:
`runs/samsung_E01_20261022T062205_061875Z/`.
It contains both PNG/SVG figures, data-quality report, normalized/paired tables,
all-field coverage, discontinuity review and complete reproducibility manifest.
Seven targeted checks passed; both figure layouts visually inspected. Raw
SHA-256 is unchanged and both raw/run paths are ignored and untracked.

Actual coverage is 2005-01-03 to 2025-01-31, with 4,949 matched dates and 237
excluded union dates. Three >5pp discount changes and one long interval remain
flagged for independent reconciliation. Direct WRDS code definitions, independent
KRX calendar/quotes, complete dated rights/actions and post-January-2025 data
remain unresolved. See `docs/DATA_ACQUISITION.md` for exact exports.

Run `.venv/Scripts/python.exe scripts/run_samsung_e01.py` to reproduce in a fresh
immutable directory. Run `.venv/Scripts/python.exe -m unittest discover -s tests
-p 'check_*.py'` for synthetic arithmetic/data-integrity/schema checks without
vendor data. `research/requirements.lock` pins research dependencies; CI is
configured to run these checks but was not executed remotely.

M0 and requested E01 figures are complete; M1 independent reconciliation remains
partial. No later milestone, predictive model, economic hypothesis test or
backtest has begun. Next action is the small validation package, then user
direction; stop after this session.


## Version 2 completed run

`runs/samsung_E01_20261022T064759_477554Z/` contains the current raw-price chart, coverage report, overlap audit, methodology snapshots and validation log. There are 5,367 matched dates through 2026-10-20; 266 excluded union dates; no overlap revisions. Eight checks passed and chart inspected. Both raw files unchanged. Adjustment panel and regressions deferred. Remaining flags are documented in the run report; prior sessions remain archived.


## Descriptive pack 20261022T070352_803683Z

Completed [EP01 figure pack](../runs/samsung/EP01_descriptive/20261022T070352_803683Z/README.md): six main/sensitivity graph pairs, flagged-episode inspection and exact tables. [Research log](RESEARCH_LOG.md) and [hypothesis tree](HYPOTHESES.md) link files. All return-based work and factors deferred. Raw source unchanged. Independent quotes/calendar and next-layer inputs remain open.


## Descriptive pack 20261022T070701_403388Z

Completed [EP01 figure pack](../runs/samsung/EP01_descriptive/20261022T070701_403388Z/README.md): six main/sensitivity graph pairs, flagged-episode inspection and exact tables. [Research log](RESEARCH_LOG.md) and [hypothesis tree](HYPOTHESES.md) link files. All return-based work and factors deferred. Raw source unchanged. Independent quotes/calendar and next-layer inputs remain open.
