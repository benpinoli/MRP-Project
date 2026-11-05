# Prediction research resume

**Current resume scope:** Start with [LONG_HORIZON_RESEARCH_PLAN.md](LONG_HORIZON_RESEARCH_PLAN.md), [LONG_HORIZON_LITERATURE.md](LONG_HORIZON_LITERATURE.md) and the reorganized tree. The user wants 2/5/10-year drivers and has held agents for review. The job records below are historical; do not resume daily forecast selection or submit prepared issuer batch J automatically.

Repository `/home/bpinoli/MRP/MRP-Project`, BYU ORC login03. Read top-level AGENTS.md, `/apps/instructions_for_ai_agents/BYU_ORC_AGENTS.md`, applicable ai-docs, implementation plan, hypothesis ledger, input audit, patch ledger, inspection and final report before continuing. Preserve the existing staged/untracked work. Do not blindly recreate a run or resubmit a pending job.

The original laptop EP01 path is absent; source pack is `runs/samsung/RG/20261026T131821Z_setup/EP01/20261026T131848_234484Z`. Config `configs/prediction/samsung_v1.json`; interpreter `.venv-rg/bin/python`; account bhb35; CPU-only, no partition, one node/core, 4GB, 10min. Raw data and all run artifacts remain local and ignored by Git.

Jobs:

- `15055217`: exploratory validation, completed exit0; numerical core loaded before source edits, end-of-run digest unreliable. Preserve.
- `15055275`: corrected validation, completed exit0; independently reviewed; executed numeric core/config unchanged but unused snapshot summary module and manifest were amended during run. Preserve/disclose.
- `15055345`: single authorized locked final evaluation, output `runs/samsung/prediction_final_15055345`; log `runs/samsung/prediction_final_15055345.log`. Read durable final report/ledger for latest state.

To inspect current state after reconnect, use the actual Slurm binaries and never query periodically more often than 60 seconds:

```bash
cd /home/bpinoli/MRP/MRP-Project
/apps/slurm/latest/bin/sacct -j 15055345 --format=JobID,State,ExitCode,Elapsed,MaxRSS -n -P
cat runs/samsung/prediction_final_15055345.log
```

If completed, inspect `metrics.csv`, `metrics_strict.csv`, `uncertainty.csv`, `stability.csv`, `predictions.csv`, `refits.json`, `provenance.json`, copied `lock.json` and `SHA256SUMS` under the final run. The independent inspection artifact records batch C verdict. Never rerun the final holdout as though untouched, and do not tune from its losses. If pending/running, wait and inspect existing output rather than submitting a duplicate. Diagnose any failure from logs before a corrected new run and label any post-test numerical correction or design change explicitly.

Final immutable source directory `runs/samsung/prediction_final_freeze`, manifest SHA256 `cbac3801f3f1cce5a3d60a2f49eb9dba6bc2d02ff98ddbe230d050522599d9af`; exclusive lock `runs/samsung/prediction_final_lock.json`, SHA256 `d41f724a64bcc893621cfa97c6d74e2c2bc3d458a1c8140c9d444a682782a26f`. Do not modify either. Selected H1 ridge alpha100 at all horizons, monthly expanding refits and strict training-label-end maturity. The final sbatch checks these hashes before/after.

Reproduction of code fixtures only (lightweight; actual empirical reruns belong in Slurm and a new directory):

```bash
export SAMSUNG_REPO="$PWD"
export PYTHONPATH="$PWD/runs/samsung/prediction_final_freeze/src"
.venv-rg/bin/python -m unittest discover -s runs/samsung/prediction_final_freeze/tests -p check_prediction.py
```

Further model development requires a predeclared bounded hypothesis and fresh unexposed evaluation dates after this run. Highest-value external dependencies are an independent historical exchange calendar, vendor availability/vintage confirmation, and qualified class spreads/flows/borrow or dividend/event panel with first-public timing. Missing mechanism branches remain untested; do not call them null. No raw data correction, publication, push, external contact or paid acquisition was authorized or performed.

Scheduler jobs persist independently; interactive research agents are not promised to survive disconnects.
