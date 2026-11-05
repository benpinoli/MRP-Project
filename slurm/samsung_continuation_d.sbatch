#!/bin/bash
#SBATCH --job-name=samsung-diag-d
#SBATCH --nodes=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=4G
#SBATCH --time=00:10:00
#SBATCH --account=bhb35
#SBATCH --output=runs/samsung/continuation_d_%j.log
set -euo pipefail
cd /home/bpinoli/MRP/MRP-Project
export SAMSUNG_REPO="$PWD" OMP_NUM_THREADS="${SLURM_CPUS_PER_TASK}" OPENBLAS_NUM_THREADS="${SLURM_CPUS_PER_TASK}" MKL_NUM_THREADS="${SLURM_CPUS_PER_TASK}" NUMEXPR_NUM_THREADS="${SLURM_CPUS_PER_TASK}"
snapshot="$PWD/runs/samsung/continuation_d_freeze"
export PYTHONPATH="$snapshot/src"
(cd "$snapshot" && echo "05623cd0e1b15b17718ef294bd6c058308294de94d45bf90579d24f87c6a0eb5  SHA256SUMS" | sha256sum -c - && sha256sum -c SHA256SUMS)
.venv-rg/bin/python -m unittest discover -s "$snapshot/tests" -p check_prediction_diagnostics.py
.venv-rg/bin/python -m samsung_research.prediction_diagnostics --config "$snapshot/config.json" --run "$PWD/runs/samsung/continuation_d_${SLURM_JOB_ID}"
(cd "$snapshot" && echo "05623cd0e1b15b17718ef294bd6c058308294de94d45bf90579d24f87c6a0eb5  SHA256SUMS" | sha256sum -c - && sha256sum -c SHA256SUMS)
