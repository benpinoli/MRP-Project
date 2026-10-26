# Samsung discount regression research hub

Specification RG 1.0.0 · 2026-10-26 · owner: researcher · status: infrastructure prepared; no empirical regression run.

This is the central entry point for the next research stage. The user's October 26 instruction supersedes the earlier descriptive-only stopping point. The observed narrowing and recent widening motivate hypotheses; they are not evidence of a particular cause. Preserve the descriptive runs and investigate changes without choosing a reversal date after seeing regression results.

## Navigation

| Artifact | Purpose |
|---|---|
| [Repository and data review](REVIEW.md) | What exists, what is trustworthy, and what needs verification |
| [Estimation methodology](METHODOLOGY.md) | Outcomes, equations, factor timing, inference and identification |
| [Literature replication map](LITERATURE.md) | Published equations versus Samsung adaptations and missing inputs |
| [Factor and mechanism dictionary](FACTORS.md) | Economic intuition, signs, exact proposed transformations and dependencies |
| [Data contracts and layout](DATA.md) | Export schemas, timestamps, licensing, missingness and provenance |
| [Cluster runbook](CLUSTER.md) | Environment setup, Slurm submission, failures and result review |
| [Cluster-side agent prompt](CLUSTER_AGENT_PROMPT.md) | Pasteable instructions for setup, verified submission and offline handoff |
| [Machine-readable specifications](../../configs/samsung_regressions.json) | Executable model definitions, sample windows, factors and inference settings |
| [Factor metadata template](../../configs/barra_metadata.example.json) | Required verification before factor data can enter a model |
| [Mechanism metadata template](../../configs/mechanisms_metadata.example.json) | Required field-level provenance for optional inputs |
| [Pipeline](../../scripts/run_samsung_regressions.py) | Readiness, preparation, one array task, collection |
| [Implementation](../../src/samsung_research/regressions.py) | Alignment, design construction, OLS and grid-aware HAC |
| [Barra export adapter](../../scripts/export_samsung_factors.py) | Uses this repo's `sf_quant.data.load_factors` on the cluster |
| [Slurm submission](../../slurm/submit_samsung_regressions.sh) | Prepare → model array → collection |
| [Validation fixtures](../../tests/check_regressions.py) | Synthetic arithmetic, timestamp, collinearity and pipeline tests |
| [Canonical methodology registry](../../methodology/methodology.json) | Versioned project-wide measures and model references |
| [Existing descriptive pack](../../runs/samsung/EP01_descriptive/20261022T070701_403388Z/README.md) | Prior figures, exact tables, audit and input manifests; local licensed artifacts |
| [Historical research log](../RESEARCH_LOG.md) / [hypotheses](../HYPOTHESES.md) | Earlier claims and H0–H7 IDs |

## Dependency-ordered work queue

| Gate | Action and acceptance condition | Owner | Status |
|---|---|---|---|
| RG0 | Review existing source hashes, class mapping and grid; preserve earlier outputs | Codex | Reviewed; independent quote/calendar checks remain open |
| RG1 | Verify Barra model ID, geography, currency, units, vintage, complete dates and historical close/availability timestamps; export on school storage | Researcher | Awaiting SSH/export; US factors may only be an explicitly approved sensitivity |
| RG2 | Stage immutable EP01 tables + manifest and factor export/timing/metadata; run preparation on compute node; inspect missingness and timestamp match report | Researcher | Code prepared |
| RG3 | Run B00–B04, main and flag-exclusion variants, HAC 5/20/60, full and prespecified calendar subsamples | Researcher | Jobs prepared; not submitted |
| RG4 | Obtain mechanism inputs by class; run L01 and M01–M04 plus joint J01 and exploratory X01/X02; compare nested models on identical samples | Researcher | Specifications prepared; missing blocks report blocked |
| RG5 | Obtain full papers and original multi-pair samples; reproduce published tables under original conventions before evaluating updated Samsung adaptations | Researcher | CK99 equation transcribed; PC19 full tables still required |
| RG6 | Extend beyond constant-beta OLS: exposure attribution, rolling estimates, event studies, stationarity/ECM, weekly/monthly aggregation, block bootstrap and chronological validation | Researcher | Design documented; separate implementation required |

## Decisions to refer back to

- Primary outcome: daily discount change in percentage points. Secondary: change in log common/preferred price ratio. A price discount is not a required discount rate.
- Barra returns are controls. They do not guarantee independent columns; OLS checks rank and conditioning and never silently drops columns.
- Full-sample residuals describe variation unexplained by the selected model. They are neither causal shocks nor out-of-sample forecasts.
- Do not translate ~5,000 daily prices into ~5,000 independent observations of annual ownership or policy changes. Use smaller, economically motivated blocks and report effective variation.
- Literature reproduction, mechanism adaptation and novel exploratory tests are different deliverables. No replication or result is claimed before its data and equation are verified.
- All empirical fitting happens after SSH on compute nodes. Local checks use synthetic data only. No backtest is included.

## Run record protocol

Each submission gets an exclusive `runs/samsung/RG/<UTC-id>/` directory. Its frozen code/configuration/methodology, input hashes, prepared panel, job list, per-task results and generated `REPORT.md` form the reviewable record. Link each reviewed report below with observations, limitations and next decision; never replace a prior run. The collector lists blocked and failed specifications and applies BH correction across the declared family of successfully estimated non-intercept coefficients (exploratory only).

No empirical run yet. Local engineering validation is recorded in [VALIDATION.md](VALIDATION.md).
