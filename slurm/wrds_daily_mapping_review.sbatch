#!/bin/bash
#SBATCH --job-name=wrds_review
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=2G
#SBATCH --time=00:10:00
#SBATCH --output=data/acquisition/2026-11-12/review_logs/review_%j.out
#SBATCH --error=data/acquisition/2026-11-12/review_logs/review_%j.err

# BYU_ORC_AGENTS.md applies; submit from the repository root.
set -euo pipefail
umask 077
module load python/3.12
python scripts/review_wrds_daily_mapping.py \
  --bundle data/acquisition/2026-11-12/wrds_daily_and_mapping \
  --descriptor data/acquisition/2026-11-11/wrds_descriptor_review \
  --archive data/acquisition/2026-11-12/wrds_daily_and_mapping_2026-11-12.zip \
  --delivery data/acquisition/2026-11-12/wrds_daily_and_mapping_2026-11-12.delivery.json \
  --output "${1:?Supply a new private output directory}"
