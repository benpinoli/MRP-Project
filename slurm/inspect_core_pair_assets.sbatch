#!/bin/bash
#SBATCH --job-name=pair_ids
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=4G
#SBATCH --time=00:10:00
#SBATCH --output=runs/core_pairs/logs/inspect_%j.out
#SBATCH --error=runs/core_pairs/logs/inspect_%j.err

set -euo pipefail

REPO="/home/bpinoli/MRP/MRP-Project"
mkdir -p "$REPO/runs/core_pairs/logs"
cd "$REPO"
export POLARS_MAX_THREADS="${SLURM_CPUS_PER_TASK}"
srun .venv/bin/python scripts/inspect_core_pair_assets.py \
  --output runs/core_pairs/asset_identity_candidates.csv
