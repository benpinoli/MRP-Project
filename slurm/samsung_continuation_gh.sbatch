#!/bin/bash
#SBATCH --job-name=samsung-gh
#SBATCH --nodes=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=4G
#SBATCH --time=00:10:00
#SBATCH --account=bhb35
#SBATCH --output=runs/samsung/continuation_gh_%j.log
set -euo pipefail
cd /home/bpinoli/MRP/MRP-Project
export SAMSUNG_REPO="$PWD" OMP_NUM_THREADS="${SLURM_CPUS_PER_TASK}" OPENBLAS_NUM_THREADS="${SLURM_CPUS_PER_TASK}" MKL_NUM_THREADS="${SLURM_CPUS_PER_TASK}" NUMEXPR_NUM_THREADS="${SLURM_CPUS_PER_TASK}"
snapshot="$PWD/runs/samsung/continuation_gh_freeze"
export PYTHONPATH="$snapshot/src"
(cd "$snapshot" && echo "a5a7edb94a50f335ca425c2f441be1a3f3333cdbab1a5846c05b1bfcccaea9fa  SHA256SUMS" | sha256sum -c - && sha256sum -c SHA256SUMS)
.venv-rg/bin/python -m unittest discover -s "$snapshot/tests" -p check_prediction_activity_range.py
.venv-rg/bin/python -m samsung_research.prediction_activity_range --config "$snapshot/config.json" --run "$PWD/runs/samsung/continuation_gh_${SLURM_JOB_ID}"
(cd "$snapshot" && echo "a5a7edb94a50f335ca425c2f441be1a3f3333cdbab1a5846c05b1bfcccaea9fa  SHA256SUMS" | sha256sum -c - && sha256sum -c SHA256SUMS)
