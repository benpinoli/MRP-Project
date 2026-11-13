#!/bin/bash
#SBATCH --job-name=loop_receive_v3
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=2G
#SBATCH --time=00:10:00
#SBATCH --output=runs/loop_long_horizon/logs/receipt_v3_%j.out
#SBATCH --error=runs/loop_long_horizon/logs/receipt_v3_%j.err
# Follow BYU_ORC_AGENTS.md. No archive overlays or paused work restart.
set -euo pipefail
umask 077
.venv-rg/bin/python scripts/receive_loop_v3.py \
  --incoming data/acquisition/2026-11-12_v1 \
  --output "runs/loop_long_horizon/v3_receipt_${SLURM_JOB_ID}"
