#!/bin/bash
#SBATCH --job-name=pair_gaps
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=4G
#SBATCH --time=00:20:00
#SBATCH --output=runs/core_pairs/logs/gaps_%j.out
#SBATCH --error=runs/core_pairs/logs/gaps_%j.err

set -euo pipefail

REPO="/home/bpinoli/MRP/MRP-Project"
cd "$REPO"
export OMP_NUM_THREADS="${SLURM_CPUS_PER_TASK}"
export OPENBLAS_NUM_THREADS="${SLURM_CPUS_PER_TASK}"
export MKL_NUM_THREADS="${SLURM_CPUS_PER_TASK}"
export NUMEXPR_NUM_THREADS="${SLURM_CPUS_PER_TASK}"
OUTPUT="runs/core_pairs/prosus_tencent_${SLURM_JOB_ID}"
srun .venv-rg/bin/python scripts/analyze_core_pair_gaps.py --output "$OUTPUT"
