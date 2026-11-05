#!/bin/bash
#SBATCH --job-name=samsung-state-f
#SBATCH --nodes=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=4G
#SBATCH --time=00:10:00
#SBATCH --account=bhb35
#SBATCH --output=runs/samsung/continuation_f_%j.log
set -euo pipefail
cd /home/bpinoli/MRP/MRP-Project
export SAMSUNG_REPO="$PWD" OMP_NUM_THREADS="${SLURM_CPUS_PER_TASK}" OPENBLAS_NUM_THREADS="${SLURM_CPUS_PER_TASK}" MKL_NUM_THREADS="${SLURM_CPUS_PER_TASK}" NUMEXPR_NUM_THREADS="${SLURM_CPUS_PER_TASK}"
snapshot="$PWD/runs/samsung/continuation_f_freeze"
export PYTHONPATH="$snapshot/src"
(cd "$snapshot" && echo "ade26c028851004389a459cad8e7bedd5cacdc6137b43a6a8bf773d60f1db54f  SHA256SUMS" | sha256sum -c - && sha256sum -c SHA256SUMS)
.venv-rg/bin/python -m unittest discover -s "$snapshot/tests" -p check_prediction_external.py
.venv-rg/bin/python -m samsung_research.prediction_external --config "$snapshot/config.json" --run "$PWD/runs/samsung/continuation_f_${SLURM_JOB_ID}"
(cd "$snapshot" && echo "ade26c028851004389a459cad8e7bedd5cacdc6137b43a6a8bf773d60f1db54f  SHA256SUMS" | sha256sum -c - && sha256sum -c SHA256SUMS)
