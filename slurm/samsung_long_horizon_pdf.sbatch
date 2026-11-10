#!/bin/bash
#SBATCH --job-name=samsung-lhpdf
#SBATCH --nodes=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=2G
#SBATCH --time=00:10:00
#SBATCH --account=bhb35
#SBATCH --output=runs/samsung/long_horizon_pdf_%j.log
set -euo pipefail
cd /home/bpinoli/MRP/MRP-Project
export SAMSUNG_REPO="$PWD" OMP_NUM_THREADS="${SLURM_CPUS_PER_TASK}" OPENBLAS_NUM_THREADS="${SLURM_CPUS_PER_TASK}" MKL_NUM_THREADS="${SLURM_CPUS_PER_TASK}" NUMEXPR_NUM_THREADS="${SLURM_CPUS_PER_TASK}"
snapshot="$PWD/runs/samsung/long_horizon_pdf_freeze"
export PYTHONPATH="$snapshot/src"
python_bin="$PWD/runs/samsung/long_horizon_tools/venv/bin/python"
(cd "$snapshot" && echo "35a854ea80c13517a713202ded5006c60fa31da4c3cc8182790228f74ca6d36a  SHA256SUMS" | sha256sum -c - && sha256sum -c SHA256SUMS)
"$python_bin" -m unittest discover -s "$snapshot/tests" -p check_long_horizon_pdf_extract.py
"$python_bin" -m samsung_research.long_horizon_pdf_extract --manifest "$snapshot/manifest.json" --run "$PWD/runs/samsung/long_horizon_pdf_${SLURM_JOB_ID}"
(cd "$snapshot" && echo "35a854ea80c13517a713202ded5006c60fa31da4c3cc8182790228f74ca6d36a  SHA256SUMS" | sha256sum -c - && sha256sum -c SHA256SUMS)
