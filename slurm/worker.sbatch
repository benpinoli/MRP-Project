#!/usr/bin/env bash
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=4G
#SBATCH --time=00:30:00
set -euo pipefail
: "${RESEARCH_REPO:?}" "${RESEARCH_PYTHON:?}" "${RG_RUN:?}" "${RG_CONFIG:?}" "${RG_SCRIPT:?}"
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
export PYTHONPATH="$RG_RUN/frozen/src"
case "${1:?Expected prepare, fit or collect}" in
  prepare) "$RESEARCH_PYTHON" "$RG_SCRIPT" prepare --repo "$RESEARCH_REPO" --config "$RG_CONFIG" --run "$RG_RUN" ;;
  fit) "$RESEARCH_PYTHON" "$RG_SCRIPT" fit --config "$RG_CONFIG" --run "$RG_RUN" --task "${SLURM_ARRAY_TASK_ID:?}" ;;
  collect) "$RESEARCH_PYTHON" "$RG_SCRIPT" collect --config "$RG_CONFIG" --run "$RG_RUN" ;;
  *) exit 2 ;;
esac
