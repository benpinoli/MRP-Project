#!/bin/bash
#SBATCH --job-name=samsung-adapt-e
#SBATCH --nodes=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=4G
#SBATCH --time=00:10:00
#SBATCH --account=bhb35
#SBATCH --output=runs/samsung/continuation_e_%j.log
set -euo pipefail
cd /home/bpinoli/MRP/MRP-Project
export SAMSUNG_REPO="$PWD" OMP_NUM_THREADS="${SLURM_CPUS_PER_TASK}" OPENBLAS_NUM_THREADS="${SLURM_CPUS_PER_TASK}" MKL_NUM_THREADS="${SLURM_CPUS_PER_TASK}" NUMEXPR_NUM_THREADS="${SLURM_CPUS_PER_TASK}"
snapshot="$PWD/runs/samsung/continuation_e_freeze"
export PYTHONPATH="$snapshot/src"
(cd "$snapshot" && echo "8fa92211f47e00b07bb75869945b99d097840c1070758177dae07d0de8bb6409  SHA256SUMS" | sha256sum -c - && sha256sum -c SHA256SUMS)
.venv-rg/bin/python -m unittest discover -s "$snapshot/tests" -p check_prediction_adaptation.py
.venv-rg/bin/python -m samsung_research.prediction_adaptation --config "$snapshot/config.json" --run "$PWD/runs/samsung/continuation_e_${SLURM_JOB_ID}"
(cd "$snapshot" && echo "8fa92211f47e00b07bb75869945b99d097840c1070758177dae07d0de8bb6409  SHA256SUMS" | sha256sum -c - && sha256sum -c SHA256SUMS)
