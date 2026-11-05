#!/bin/bash
#SBATCH --job-name=samsung-archive-i
#SBATCH --nodes=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=1G
#SBATCH --time=00:05:00
#SBATCH --account=bhb35
#SBATCH --output=runs/samsung/continuation_i_%j.log
set -euo pipefail
cd /home/bpinoli/MRP/MRP-Project
export SAMSUNG_REPO="$PWD" OMP_NUM_THREADS="${SLURM_CPUS_PER_TASK}" OPENBLAS_NUM_THREADS="${SLURM_CPUS_PER_TASK}" MKL_NUM_THREADS="${SLURM_CPUS_PER_TASK}" NUMEXPR_NUM_THREADS="${SLURM_CPUS_PER_TASK}"
snapshot="$PWD/runs/samsung/continuation_i_freeze"
export PYTHONPATH="$snapshot/src"
(cd "$snapshot" && echo "d0378690b673028290d81cedabf319484e5a42b7b2f02a5d8ae758d773db809f  SHA256SUMS" | sha256sum -c - && sha256sum -c SHA256SUMS)
.venv-rg/bin/python -m unittest discover -s "$snapshot/tests" -p check_prediction_candidate_archive.py
.venv-rg/bin/python -m samsung_research.prediction_candidate_archive --config "$snapshot/config.json" --run "$PWD/runs/samsung/continuation_i_${SLURM_JOB_ID}"
(cd "$snapshot" && echo "d0378690b673028290d81cedabf319484e5a42b7b2f02a5d8ae758d773db809f  SHA256SUMS" | sha256sum -c - && sha256sum -c SHA256SUMS)
