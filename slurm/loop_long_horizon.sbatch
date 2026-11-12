#!/bin/bash
#SBATCH --job-name=loop_lh
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=2G
#SBATCH --time=00:20:00
#SBATCH --output=runs/loop_long_horizon/logs/research_%j.out
#SBATCH --error=runs/loop_long_horizon/logs/research_%j.err

# See BYU_ORC_AGENTS.md. Submit from repository root; do not restart other jobs.
set -euo pipefail
umask 077
export OMP_NUM_THREADS="$SLURM_CPUS_PER_TASK"
export OPENBLAS_NUM_THREADS="$SLURM_CPUS_PER_TASK"
export MKL_NUM_THREADS="$SLURM_CPUS_PER_TASK"
export NUMEXPR_NUM_THREADS="$SLURM_CPUS_PER_TASK"
.venv-rg/bin/python tests/check_loop_long_horizon.py
.venv-rg/bin/python scripts/run_loop_long_horizon.py \
  --config configs/loop_long_horizon_v1.json \
  --output "runs/loop_long_horizon/${SLURM_JOB_ID}"
