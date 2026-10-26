# Cluster runbook

The researcher handles SSH. Nothing has been submitted or estimated on the school cluster. No school hostname, Slurm allocation, partition or module name has been assumed. Jobs use CPU only: 1 core, 4 GB, 30 minutes, at most 8 concurrent tasks by default. These daily OLS designs are small; Slurm provides orderly reproducibility, not a need for distributed matrix algebra.

## 1. Stage the repository and environment

From the Linux cluster shell, enter the repository. Use Python 3.11–3.13 and the school's approved module/environment procedure. The minimal regression dependencies are separate from the full optimization/backtest library:

```bash
python3 -m venv .venv-rg
.venv-rg/bin/python -m pip install -r research/regression-requirements.lock
cp slurm/cluster.env.example.sh slurm/cluster.env.sh
# Edit RESEARCH_REPO, RESEARCH_PYTHON and your site's optional account/partition.
```

For the sf-quant export, use the existing project environment from `uv sync --frozen` (if uv is supported), or an equivalent environment provisioned from the existing `uv.lock`. Add the minimal regression requirements if needed. Set ROOT and DATABASE privately according to the school's storage configuration. No database credentials are required to fit staged CSV files.

Transfer/recreate the ignored EP01 run and raw source on authorized storage, with hashes verified; a Git checkout alone does not contain them. Either place the exact run under the configured path or create a new config identifying an independently reproduced EP01 run. Keep old outputs in place.

## 2. Export and verify factors

Using the project environment with access to the school data:

```bash
python scripts/export_samsung_factors.py --start 2004-12-20 --end 2026-10-20 \
  --output data/regression/raw/barra/factors.csv
mkdir -p data/regression/metadata
cp configs/barra_metadata.example.json data/regression/metadata/barra.json
```

The export is not a model-coverage audit. Complete the metadata and supply source factor calendar, timing and Korean session-close files according to [DATA.md](DATA.md). The default factor list is a US-model sensitivity and will block until explicitly acknowledged; use a verified Korea/global model for the preferred specification and replace factor names in a versioned config. If that model is not exposed by `sf_quant.load_factors`, export its licensed wide returns separately into the same contract. `X02` must also name the selected model's verified chip factor.

Optional mechanisms can arrive later; each absent block is clearly recorded as blocked. A malformed supplied block fails preparation so incorrect provenance cannot silently disappear.

## 3. Check, submit and inspect

Readiness checks paths only; preparation performs the substantive validation on a compute node.

```bash
.venv-rg/bin/python scripts/run_samsung_regressions.py readiness
.venv-rg/bin/python -m unittest discover -s tests -p check_regressions.py
bash slurm/submit_samsung_regressions.sh slurm/cluster.env.sh
```

There are 312 tasks in the default grid: 13 models × 2 data variants × 4 windows × 3 HAC bandwidths. The submission script creates a new run, freezes code/config/docs/dependencies, submits preparation, submits a capped array with `afterok`, then collection with `afterany`. This follows [official Slurm array/dependency semantics](https://slurm.schedmd.com/job_array.html). Site policy may require adjusting resources in `worker.sbatch` before submission. Files have LF endings via `.gitattributes`; invoke scripts with bash, no executable-bit assumption.

Use the saved `jobs.txt` with `squeue -u "$USER"` and `sacct -j JOB_ID --format=JobID,State,ExitCode,Elapsed,MaxRSS`. Review preparation logs and `prepared/readiness.json` first. Every fitted task saves coefficient uncertainty, residuals, diagnostics and exact sample dates. `REPORT.md`, `coefficients.csv`, and `status.json` are generated at the run root; link that report in the [hub](README.md) after human review.

## 4. Failure and rerun policy

Missing/invalid required inputs stop preparation. The fit array's `afterok` prevents fitting an invalid panel; invalid dependencies are cancelled on supporting Slurm configurations. If preparation fails before `tasks.json` is written, collection also cannot produce a complete report; read preparation logs/readiness, correct inputs, and submit a NEW run. Runtime failures and missing tasks are reported by collection and cause its nonzero exit. Missing optional fields, insufficient sample size or collinear designs are blocked outcomes, not successful null estimates; they do not crash unrelated models.

Do not resubmit into an existing task directory; exclusive creation protects run history. For a model change, corrected input, or retry, make a new submission. Review all exclusions and common-sample nested fits before interpreting incremental explanation. No job automatically publishes, commits, sends notifications or opens a connection to the cluster.
