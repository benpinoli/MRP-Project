#!/bin/bash
#SBATCH --job-name=samsung-predict-v2
#SBATCH --nodes=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=4G
#SBATCH --time=00:10:00
#SBATCH --account=bhb35
#SBATCH --output=runs/samsung/prediction_validation_v2_%j.log
set -euo pipefail
cd /home/bpinoli/MRP/MRP-Project
export SAMSUNG_REPO="$PWD" OMP_NUM_THREADS="${SLURM_CPUS_PER_TASK}" OPENBLAS_NUM_THREADS="${SLURM_CPUS_PER_TASK}" MKL_NUM_THREADS="${SLURM_CPUS_PER_TASK}" NUMEXPR_NUM_THREADS="${SLURM_CPUS_PER_TASK}"
snapshot="$PWD/runs/samsung/prediction_freeze_v2"
export PYTHONPATH="$snapshot/src"
(cd "$snapshot" && sha256sum -c SHA256SUMS)
.venv-rg/bin/python -m unittest discover -s "$snapshot/tests" -p check_prediction.py
.venv-rg/bin/python -m samsung_research.prediction --config "$snapshot/config.json" --run "runs/samsung/prediction_v2_${SLURM_JOB_ID}" --mode validation
(cd "$snapshot" && sha256sum -c SHA256SUMS)
