# Engineering validation — 2026-10-26

No Samsung empirical regression was fitted. No cluster login, submission or factor export was performed.

- All 21 checks pass with `python -m unittest discover -s tests -p 'check_*.py'`: 13 existing data/descriptive/methodology checks and 8 new regression engineering checks.
- Synthetic regression checks cover a hand-calculated discount/log-gap change, no gap bridging, foreign holiday aggregation, late availability rejection, missing factor values, timezone requirements, OLS coefficients, an independent HAC score calculation, original-grid HAC distances, rank/constant/small-sample rejection, configuration names/grid, exclusion of private cluster settings from snapshots, and prepare→fit→collect/tampering behavior.
- The configuration has 13 unique model IDs and 312 tasks. Default factor names exist in the shipped static sf-quant list; live availability/model metadata remain unverified.
- Methodology 4.0.0 validates against the extended JSON Schema and exactly matches generated `docs/METHODOLOGY.md`. Existing descriptive definitions and archived run snapshots are preserved.
- The active raw file's SHA-256 matches `c64a9cdbba02ee7d70cd3fa4b0af14e0540d0beab70d3d55132f333fb11ba8bb`. No raw prices or earlier runs were modified.
- Readiness correctly identifies the five required unstaged files: factor export, factor timing, source factor calendar, Korean sessions/close times, and reviewed Barra metadata. Optional mechanism models remain conditional on their inputs.

Local Windows sandbox temporary storage was unavailable on the initial test attempt. Tests passed using an ignored workspace `runs/regression-validation-temp/` directory for TEMP/TMP; this required no test or production behavior change. Cluster tests use normal Linux temporary storage.

All three shell files independently pass Git Bash `-n`: submission script, worker and cluster-profile example. Git Bash required execution outside the Windows sandbox because its MSYS startup was blocked there. No `sbatch` command was executed, so scheduler behavior and site resource policies still need verification on the school cluster. CI has been updated to install the regression dependency set and run each Bash syntax check on Linux; CI itself has not been run remotely.

All local links in the regression documentation resolve. The three reused EP01 artifact hashes (both measure tables and the source-inventory snapshot) match their immutable manifest. `git diff --check` is clean after methodology regeneration.
