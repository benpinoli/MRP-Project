#!/bin/bash
#SBATCH --job-name=loop_lh_v4
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=2G
#SBATCH --time=00:10:00
#SBATCH --output=runs/loop_long_horizon/logs/research_v4_%j.out
#SBATCH --error=runs/loop_long_horizon/logs/research_v4_%j.err
# Follow BYU_ORC_AGENTS.md. Existing forecasts only; preserve prior results.
set -euo pipefail
umask 077
export OMP_NUM_THREADS="$SLURM_CPUS_PER_TASK"
export OPENBLAS_NUM_THREADS="$SLURM_CPUS_PER_TASK"
export MKL_NUM_THREADS="$SLURM_CPUS_PER_TASK"
export NUMEXPR_NUM_THREADS="$SLURM_CPUS_PER_TASK"
.venv-rg/bin/python tests/check_loop_v4.py
.venv-rg/bin/python scripts/run_loop_v4.py \
  --config configs/loop_long_horizon_v4.json \
  --output "runs/loop_long_horizon/v4_${SLURM_JOB_ID}"
