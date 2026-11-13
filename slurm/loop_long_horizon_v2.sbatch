#!/bin/bash
#SBATCH --job-name=loop_lh_v2
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=512M
#SBATCH --time=00:05:00
#SBATCH --output=runs/loop_long_horizon/logs/stability_%j.out
#SBATCH --error=runs/loop_long_horizon/logs/stability_%j.err

# Follow BYU_ORC_AGENTS.md; independent diagnostics, no paused work restart.
set -euo pipefail
umask 077
export OMP_NUM_THREADS="$SLURM_CPUS_PER_TASK"
export OPENBLAS_NUM_THREADS="$SLURM_CPUS_PER_TASK"
export MKL_NUM_THREADS="$SLURM_CPUS_PER_TASK"
export NUMEXPR_NUM_THREADS="$SLURM_CPUS_PER_TASK"
.venv-rg/bin/python tests/check_loop_stability.py
.venv-rg/bin/python scripts/check_loop_stability.py \
  --config configs/loop_long_horizon_v2.json \
  --output "runs/loop_long_horizon/v2_${SLURM_JOB_ID}"
