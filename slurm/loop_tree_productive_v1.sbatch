#!/bin/bash
#SBATCH --job-name=loop_tree_productive
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=2G
#SBATCH --time=00:10:00
#SBATCH --output=runs/loop_long_horizon/logs/tree_productive_%j.out
#SBATCH --error=runs/loop_long_horizon/logs/tree_productive_%j.err
# Follow BYU_ORC_AGENTS.md; one frozen finite batch, preserve original sources.
set -euo pipefail
umask 077
export OMP_NUM_THREADS=1
export OPENBLAS_NUM_THREADS=1
export MKL_NUM_THREADS=1
.venv-rg/bin/python scripts/run_loop_tree_batch_v1.py \
  --config configs/loop_tree_productive_batch_v1.json \
  --output "runs/loop_long_horizon/tree_productive_${SLURM_JOB_ID}"
