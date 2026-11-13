#!/bin/bash
#SBATCH --job-name=loop_lh5_mean
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=1G
#SBATCH --time=00:10:00
#SBATCH --output=runs/loop_long_horizon/logs/research_v5_%j.out
#SBATCH --error=runs/loop_long_horizon/logs/research_v5_%j.err
# Follow BYU_ORC_AGENTS.md. One predeclared quasi-mean test; preserve prior runs.
set -euo pipefail
umask 077
export OMP_NUM_THREADS="$SLURM_CPUS_PER_TASK"
export OPENBLAS_NUM_THREADS="$SLURM_CPUS_PER_TASK"
export MKL_NUM_THREADS="$SLURM_CPUS_PER_TASK"
.venv-rg/bin/python tests/check_positive_ratio_mean.py
.venv-rg/bin/python scripts/run_loop_v5.py \
  --config configs/loop_long_horizon_v5.json \
  --output "runs/loop_long_horizon/v5_${SLURM_JOB_ID}"
