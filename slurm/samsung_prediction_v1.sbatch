#!/bin/bash
#SBATCH --job-name=samsung-predict
#SBATCH --nodes=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=4G
#SBATCH --time=00:30:00
#SBATCH --account=bhb35
#SBATCH --output=runs/samsung/prediction_validation_%j.log
set -euo pipefail
cd /home/bpinoli/MRP/MRP-Project
export OMP_NUM_THREADS="${SLURM_CPUS_PER_TASK}" OPENBLAS_NUM_THREADS="${SLURM_CPUS_PER_TASK}" MKL_NUM_THREADS="${SLURM_CPUS_PER_TASK}" NUMEXPR_NUM_THREADS="${SLURM_CPUS_PER_TASK}" PYTHONPATH=src
.venv-rg/bin/python -m unittest tests.check_prediction
.venv-rg/bin/python -m samsung_research.prediction --run "runs/samsung/prediction_v1_${SLURM_JOB_ID}" --mode validation
