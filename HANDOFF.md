
# Samsung Regression Cluster Handoff

This note records what ran on BYU ORC and how to continue. No regression fit array or collection job has been submitted, and no regression coefficients/results exist.

## What completed

- Checkout was on `login01`, branch `main`, commit `3d2b8faecbbeed8e0fe0b496d0e775fb3d82bebc`; it was clean before this setup. `git fetch origin` and `git merge --ff-only origin/main` found it already current.
- Provisioned `.venv-rg` with Python 3.11.11 and the research dependency lists:
  `uv venv --python /usr/bin/python3.11 .venv-rg`
  `uv pip install --python .venv-rg/bin/python -r research/regression-requirements.lock -r research/requirements.lock`
- Provisioned project `.venv` from `uv.lock` for `sf_quant`:
  `uv sync --frozen --python /usr/bin/python3.11 --no-dev`
- Found the licensed raw source at `src/sf_quant/data/samsung_2005-20261020.csv`. Its SHA-256 is `c64a9cdbba02ee7d70cd3fa4b0af14e0540dbeab70d3d55132f333fb11ba8bb`, matching the registered hash.
- Ran Slurm job `14766421` on `m8-17-6`. It passed all 21 `check_*.py` tests and `bash -n` checks, reproduced EP01, and ran regression readiness. It completed exit code 0 in 1:51.
- EP01 output is under `runs/samsung/RG/20261026T131821Z_setup/EP01/20261026T131848_234484Z/`. The source and generated output hashes/table checks passed in the independent verifier; its last check failed because this nested location makes existing README relative links resolve incorrectly. The verifier log is `runs/samsung/RG/20261026T131821Z_setup/logs/ep01-verification.log`.
- Readiness enumerated 312 configurations but reported blocked; it ran no empirical regression. See `runs/samsung/RG/20261026T131821Z_setup/logs/readiness.json`.

## What failed

Factor export job `14766427` was accepted by Slurm and finished, but the export itself failed. The job script set `ROOT=/home/bpinoli` and `DATABASE=production` without exporting them, so `sf_quant` reported `ROOT, DATABASE not set`. No factor CSV was created. See `runs/samsung/RG/20261026T131821Z_setup/logs/factor-export.log`.

The export is reproducible after supplying those settings to the process, for example by adding these lines to `runs/samsung/RG/20261026T131821Z_setup/export.sbatch` before calling Python:

```bash
export ROOT=/home/bpinoli
export DATABASE=production
```

Then submit that export script on a compute node. The repository's adapter uses `sf_quant.data.load_factors`, as required. This only produces factor returns; it does not establish model geography, return timing, availability or an independent calendar.

## Exact remaining requirements

Readiness listed these missing required inputs:

- `data/regression/raw/barra/factors.csv` — retry the factor export and preserve its export metadata.
- `data/regression/metadata/factor_calendar.csv` — independently sourced expected factor sessions and covered date range; do not derive it from observed factor rows.
- `data/regression/metadata/factor_timing.csv` — actual return period-end and vendor availability UTC timestamps for every factor date.
- `data/regression/metadata/sessions.csv` — verified historical Korean close UTC times for each EP01 observed session, including historical/special closes.
- `data/regression/metadata/barra.json` — reviewed model identity, geography/Korea coverage, currency and justification, units, vintage, source references and sensitivity acknowledgement as applicable.

School-side `/home/bpinoli/groups/grp_quant/sf-data-pipelines/docs/BARRA.md` documents US USSLOWL datasets. It does not verify Korean coverage, Korean-vs-US timing, publication availability or the independent calendar. Do not fill these fields by assumption. Optional mechanism datasets can be absent; their models will be reported blocked.

## How to recreate the completed setup

From the repository root on `login01`, after confirming the current branch and local changes:

```bash
git status --short --branch
git fetch origin
git merge --ff-only origin/main
sha256sum src/sf_quant/data/samsung_2005-20261020.csv
uv venv --python /usr/bin/python3.11 .venv-rg
uv pip install --python .venv-rg/bin/python -r research/regression-requirements.lock -r research/requirements.lock
uv sync --frozen --python /usr/bin/python3.11 --no-dev
```

The completed job scripts and logs are retained in `runs/samsung/RG/20261026T131821Z_setup/`. The setup Slurm job was submitted as:

```bash
/apps/slurm/latest/bin/sacct -j 14766421,14766427 --format=JobID,State,ExitCode,Elapsed,MaxRSS
```

Both scheduler jobs completed with exit status 0, but job `14766427`'s export command failed as described above. The setup job command was `sbatch --account=bhb35 --job-name=samsung-setup .../setup.sbatch`; it ran tests, recreated EP01, then ran regression readiness. The factor-export job was `sbatch --account=bhb35 --dependency=afterany:14766421 --job-name=samsung-factor-export .../export.sbatch`.

## Steps after inputs are genuinely available

1. Fix and rerun the factor export with environment variables exported; confirm `factors.csv` and its metadata hash/date coverage.
2. Obtain supporting school/vendor/exchange documentation for factor identity, units/currency, actual timestamp convention and release availability; gather the independently sourced factor calendar and historical KRX close schedule. Populate and review metadata based on that evidence.
3. Put the verified inputs in the paths above. Run `.venv-rg/bin/python scripts/run_samsung_regressions.py readiness --config <versioned-config.json>` and resolve every required-input or metadata gate. Do not submit the fit grid while readiness is blocked.
4. Configure the ignored `slurm/cluster.env.sh` with the repository path, `.venv-rg/bin/python`, and the site-approved account. Use a separate versioned config pointing at the reproduced EP01 output if the default run is not canonical.
5. Once readiness genuinely passes, run `bash slurm/submit_samsung_regressions.sh slurm/cluster.env.sh`. Verify the returned prepare, array and collector IDs using `squeue`/`sacct` and verify the dependency chain. Preparation must succeed before relying on the array.
6. When fitting finishes, inspect the run's `REPORT.md`, `status.json`, `coefficients.csv`, and Slurm logs. Review blocked mechanism models separately.

No fit array or collector ID exists. Relevant records and logs are in `runs/samsung/RG/20261026T131821Z_setup/`.
