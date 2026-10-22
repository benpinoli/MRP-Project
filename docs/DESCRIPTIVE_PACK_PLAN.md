# Samsung descriptive figure pack plan

User-authorized scope: six descriptive figures, visible gaps, a flag-exclusion
sensitivity version, local inspection of flagged episodes, and navigable logs.
The observed preferred discount is not an estimate of vote value. No factor
regressions, adjusted returns, total returns or backtests.

1. Reuse the validated immutable v2 raw input and identity/status rules. Create
   a fresh grouped run under `runs/samsung/EP01_descriptive/<UTC run>/`.
2. Register definitions before execution. Define sessions as observed dates
   where at least one local class has an eligible quote; retain missing pairs
   on that grid. This is a session proxy, pending an independent KRX calendar.
3. Calculate percentage-point changes between adjacent proxy sessions only.
   Use trailing sample standard deviation of discount changes over 20 proxy
   sessions, ddof=1, minimum 20 finite changes, unannualized. Never compress
   missing or flagged dates out of rolling windows or difference calculations.
4. Flag audit jumps/long intervals, code-5/volume conflicts, asymmetric source
   rows and absent-both weekdays. Keep flagged but valid values in main plots;
   remove flagged dates before summary/difference/window calculations in the
   sensitivity version. Top-ten largest-change highlighting is descriptive,
   not an extra exclusion rule. Split marker is context, not a suspicious flag.
5. Produce six PNG/SVG figures for each version. Annual boxplots show median,
   interquartile range, 1.5-IQR whiskers and outliers; mark partial 2026. Recent
   raw-price panels start in 2019. Volume panels are raw actual shares by class
   and preferred/common ratio, not liquidity. Do not fill missing volume.
6. Save flagged-date tables, local quote/status/volume windows, episode plots,
   numerical summaries and an inspection report with unresolved explanations.
7. Visually inspect all plot layouts, run meaningful arithmetic/window/gap
   checks and hash checks. Update canonical methodology, append-only logs,
   experiment record and artifact catalog. Generate clickable research and
   hypothesis indexes linking each output and archived run without moving or
   rewriting earlier run directories.

Completed under methodology 3.0.1 in
`runs/samsung/EP01_descriptive/20261022T070701_403388Z/`. Thirteen tests passed.
All six main/sensitivity layouts were inspected; the local long-gap display was
corrected and checked in the final run. Exact output arithmetic and local links
verified independently. The prior pack remains indexed as superseded for the
episode display. See [research log](RESEARCH_LOG.md) for figures and review status.

Acceptance: one command reproduces the pack from configured local raw data;
all outputs have figure/measure IDs and filenames; sensitivity retains gaps;
documentation and registry agree; full run manifests identify code/input
versions. Earlier v1 adjusted panels remain archived and clearly deferred.
