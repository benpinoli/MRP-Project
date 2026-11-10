#!/bin/bash
#SBATCH --job-name=hypothesis-resolution
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=4G
#SBATCH --time=00:15:00
#SBATCH --account=bhb35
#SBATCH --output=runs/hypothesis_resolution/logs/%j.out
#SBATCH --error=runs/hypothesis_resolution/logs/%j.err

set -euo pipefail
cd /home/bpinoli/MRP/MRP-Project
export SAMSUNG_REPO="$PWD"
export PYTHONPATH="$PWD/src"
export OMP_NUM_THREADS="${SLURM_CPUS_PER_TASK}"
export OPENBLAS_NUM_THREADS="${SLURM_CPUS_PER_TASK}"
export MKL_NUM_THREADS="${SLURM_CPUS_PER_TASK}"
export NUMEXPR_NUM_THREADS="${SLURM_CPUS_PER_TASK}"

run="$PWD/runs/hypothesis_resolution/${SLURM_JOB_ID}"
mkdir -p "$PWD/runs/hypothesis_resolution/logs"

.venv-rg/bin/python -m unittest tests/check_hypothesis_resolution.py tests/check_issuer_event_descriptive.py
.venv-rg/bin/python -m samsung_research.issuer_event_descriptive \
  --config configs/prediction_continuation/issuer_events_j_v1.json \
  --run "$run/issuer_events"
.venv-rg/bin/python -m samsung_research.hypothesis_resolution \
  --config configs/hypothesis_resolution_v1.json \
  --issuer-run "runs/hypothesis_resolution/${SLURM_JOB_ID}/issuer_events" \
  --output "runs/hypothesis_resolution/${SLURM_JOB_ID}/results"
