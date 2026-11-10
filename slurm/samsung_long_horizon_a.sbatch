#!/bin/bash
#SBATCH --job-name=samsung-lha
#SBATCH --nodes=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=2G
#SBATCH --time=00:10:00
#SBATCH --account=bhb35
#SBATCH --output=runs/samsung/long_horizon_a_%j.log
set -euo pipefail
cd /home/bpinoli/MRP/MRP-Project
export SAMSUNG_REPO="$PWD" OMP_NUM_THREADS="${SLURM_CPUS_PER_TASK}" OPENBLAS_NUM_THREADS="${SLURM_CPUS_PER_TASK}" MKL_NUM_THREADS="${SLURM_CPUS_PER_TASK}" NUMEXPR_NUM_THREADS="${SLURM_CPUS_PER_TASK}"
snapshot="$PWD/runs/samsung/long_horizon_a_freeze"
export PYTHONPATH="$snapshot/src"
(cd "$snapshot" && echo "a65b0e14994aad2a7a3e9c24653c961a42fedb7d991efd55f553f50def62fbef  SHA256SUMS" | sha256sum -c - && sha256sum -c SHA256SUMS)
.venv-rg/bin/python -m unittest discover -s "$snapshot/tests" -p check_long_horizon_map.py
.venv-rg/bin/python -m samsung_research.long_horizon_map --config "$snapshot/config.json" --run "$PWD/runs/samsung/long_horizon_a_${SLURM_JOB_ID}"
(cd "$snapshot" && echo "a65b0e14994aad2a7a3e9c24653c961a42fedb7d991efd55f553f50def62fbef  SHA256SUMS" | sha256sum -c - && sha256sum -c SHA256SUMS)
