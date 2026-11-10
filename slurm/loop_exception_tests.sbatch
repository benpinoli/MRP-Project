#!/bin/bash
#SBATCH --job-name=loop_tests
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=8G
#SBATCH --time=00:30:00
#SBATCH --output=runs/loop_exceptions/logs/loop_%j.out
#SBATCH --error=runs/loop_exceptions/logs/loop_%j.err

set -euo pipefail
REPO="/home/bpinoli/MRP/MRP-Project"
cd "$REPO"
export OMP_NUM_THREADS="${SLURM_CPUS_PER_TASK}"
export OPENBLAS_NUM_THREADS="${SLURM_CPUS_PER_TASK}"
export MKL_NUM_THREADS="${SLURM_CPUS_PER_TASK}"
export NUMEXPR_NUM_THREADS="${SLURM_CPUS_PER_TASK}"
OUTPUT="runs/loop_exceptions/${SLURM_JOB_ID}/results"
srun .venv-rg/bin/python -m unittest tests/check_core_pair_baselines.py
srun .venv/bin/python -m unittest tests/check_loop_exception_tests.py
srun .venv-rg/bin/python scripts/run_core_pair_baselines.py --output "runs/core_pairs/validation_${SLURM_JOB_ID}"
srun .venv/bin/python scripts/run_loop_exception_tests.py --output "$OUTPUT"
