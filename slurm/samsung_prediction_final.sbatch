#!/bin/bash
#SBATCH --job-name=samsung-predict-final
#SBATCH --nodes=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=4G
#SBATCH --time=00:10:00
#SBATCH --account=bhb35
#SBATCH --output=runs/samsung/prediction_final_%j.log
set -euo pipefail
cd /home/bpinoli/MRP/MRP-Project
export SAMSUNG_REPO="$PWD" OMP_NUM_THREADS="${SLURM_CPUS_PER_TASK}" OPENBLAS_NUM_THREADS="${SLURM_CPUS_PER_TASK}" MKL_NUM_THREADS="${SLURM_CPUS_PER_TASK}" NUMEXPR_NUM_THREADS="${SLURM_CPUS_PER_TASK}"
snapshot="$PWD/runs/samsung/prediction_final_freeze"
lock="$PWD/runs/samsung/prediction_final_lock.json"
run="$PWD/runs/samsung/prediction_final_${SLURM_JOB_ID}"
test -f "$lock"
echo "d41f724a64bcc893621cfa97c6d74e2c2bc3d458a1c8140c9d444a682782a26f  $lock" | sha256sum -c -
export PYTHONPATH="$snapshot/src"
(cd "$snapshot" && echo "cbac3801f3f1cce5a3d60a2f49eb9dba6bc2d02ff98ddbe230d050522599d9af  SHA256SUMS" | sha256sum -c - && sha256sum -c SHA256SUMS)
.venv-rg/bin/python -m unittest discover -s "$snapshot/tests" -p check_prediction.py
.venv-rg/bin/python -m samsung_research.prediction --config "$snapshot/config.json" --run "$run" --mode test --lock "$lock"
cp "$lock" "$run/lock.json"
cp "$snapshot/SHA256SUMS" "$run/snapshot_SHA256SUMS"
.venv-rg/bin/python -m samsung_research.prediction_uncertainty --run "$run" --lock "$lock" --ep01 "$PWD/runs/samsung/RG/20261026T131821Z_setup/EP01/20261026T131848_234484Z"
(cd "$snapshot" && echo "cbac3801f3f1cce5a3d60a2f49eb9dba6bc2d02ff98ddbe230d050522599d9af  SHA256SUMS" | sha256sum -c - && sha256sum -c SHA256SUMS)
echo "d41f724a64bcc893621cfa97c6d74e2c2bc3d458a1c8140c9d444a682782a26f  $lock" | sha256sum -c -
