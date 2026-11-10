#!/bin/bash
#SBATCH --job-name=prosus_returns
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=2G
#SBATCH --time=00:15:00
#SBATCH --output=runs/prosus_tencent/slurm-%j.out
#SBATCH --error=runs/prosus_tencent/slurm-%j.err

set -euo pipefail
cd /home/bpinoli/MRP/MRP-Project
export OPENBLAS_NUM_THREADS=1
export OMP_NUM_THREADS=1
export MKL_NUM_THREADS=1
.venv/bin/python scripts/analyze_prosus_tencent_returns.py --config configs/prosus_tencent_return_regressions.v1.json --run-id "${SLURM_JOB_ID}"
