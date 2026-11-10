#!/bin/bash
#SBATCH --job-name=samsung-lhb
#SBATCH --nodes=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=2G
#SBATCH --time=00:10:00
#SBATCH --account=bhb35
#SBATCH --output=runs/samsung/long_horizon_b_%j.log
set -euo pipefail
cd /home/bpinoli/MRP/MRP-Project
export SAMSUNG_REPO="$PWD" OMP_NUM_THREADS="${SLURM_CPUS_PER_TASK}" OPENBLAS_NUM_THREADS="${SLURM_CPUS_PER_TASK}" MKL_NUM_THREADS="${SLURM_CPUS_PER_TASK}" NUMEXPR_NUM_THREADS="${SLURM_CPUS_PER_TASK}"
snapshot="$PWD/runs/samsung/long_horizon_b_freeze"
export PYTHONPATH="$snapshot/src"
(cd "$snapshot" && echo "35e226c53a9418ac43ff0a396959cae5827e7e8f97e6d4e0cff12240b2ad2dbe  SHA256SUMS" | sha256sum -c - && sha256sum -c SHA256SUMS)
.venv-rg/bin/python -m unittest discover -s "$snapshot/tests" -p check_long_horizon_supply.py
.venv-rg/bin/python -m samsung_research.long_horizon_supply --config "$snapshot/config.json" --run "$PWD/runs/samsung/long_horizon_b_${SLURM_JOB_ID}"
(cd "$snapshot" && echo "35e226c53a9418ac43ff0a396959cae5827e7e8f97e6d4e0cff12240b2ad2dbe  SHA256SUMS" | sha256sum -c - && sha256sum -c SHA256SUMS)
