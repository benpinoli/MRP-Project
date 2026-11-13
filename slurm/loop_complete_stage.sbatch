#!/bin/bash
#SBATCH --job-name=loop_stage_v4
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=2G
#SBATCH --time=00:10:00
#SBATCH --output=runs/loop_long_horizon/logs/complete_stage_%j.out
#SBATCH --error=runs/loop_long_horizon/logs/complete_stage_%j.err
# Follow BYU_ORC_AGENTS.md; stage private content without flattening paths.
set -euo pipefail
umask 077
.venv-rg/bin/python scripts/receive_loop_complete.py \
  --archive data/acquisition/2026-11-12_v1/wrds_complete_transfer_2026-11-12_v1.zip \
  --stage "data/acquisition/complete_transfer_v4_${SLURM_JOB_ID}" \
  --output "runs/loop_long_horizon/v4_receipt_${SLURM_JOB_ID}"
