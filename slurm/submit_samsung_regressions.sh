#!/usr/bin/env bash
set -euo pipefail
profile=${1:-slurm/cluster.env.sh}
if [[ ! -f "$profile" ]]; then
  printf 'Create %s from slurm/cluster.env.example.sh first.\n' "$profile" >&2
  exit 2
fi
source "$profile"
: "${RESEARCH_REPO:?Set absolute repository path}"
: "${RESEARCH_PYTHON:?Set absolute Python executable}"
cd "$RESEARCH_REPO"
export RESEARCH_REPO RESEARCH_PYTHON
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
export PYTHONPATH="$RESEARCH_REPO/src${PYTHONPATH:+:$PYTHONPATH}"
config=${RG_CONFIG:-configs/samsung_regressions.json}
export RG_RUN="$RESEARCH_REPO/runs/samsung/RG/$(date -u +%Y%m%dT%H%M%S)_${RANDOM}"
"$RESEARCH_PYTHON" scripts/run_samsung_regressions.py freeze --repo "$RESEARCH_REPO" --config "$config" --run "$RG_RUN"
mkdir -p "$RG_RUN/logs"
export RG_CONFIG="$RG_RUN/frozen/config.json"
export RG_SCRIPT="$RG_RUN/frozen/scripts/run_samsung_regressions.py"
export PYTHONPATH="$RG_RUN/frozen/src"
n=$("$RESEARCH_PYTHON" "$RG_SCRIPT" count --config "$RG_CONFIG")
opts=(--parsable --export=ALL --chdir="$RESEARCH_REPO")
[[ -z "${SLURM_ACCOUNT:-}" ]] || opts+=(--account="$SLURM_ACCOUNT")
[[ -z "${SLURM_PARTITION:-}" ]] || opts+=(--partition="$SLURM_PARTITION")
worker="$RG_RUN/frozen/slurm/worker.sbatch"
prep=$(sbatch "${opts[@]}" --job-name=samsung-rg-prep --output="$RG_RUN/logs/prepare_%j.log" "$worker" prepare)
prep=${prep%%;*}
array=$(sbatch "${opts[@]}" --job-name=samsung-rg-fit --output="$RG_RUN/logs/fit_%A_%a.log" --array="0-$((n-1))%${RG_CONCURRENCY:-8}" --dependency="afterok:$prep" --kill-on-invalid-dep=yes "$worker" fit)
array=${array%%;*}
# afterany ensures a report is generated even when a worker crashes.
summary=$(sbatch "${opts[@]}" --job-name=samsung-rg-report --output="$RG_RUN/logs/collect_%j.log" --dependency="afterany:$array" "$worker" collect)
summary=${summary%%;*}
printf 'prepare=%s\narray=%s\ncollect=%s\n' "$prep" "$array" "$summary" > "$RG_RUN/jobs.txt"
printf 'Run: %s\nPrepare: %s; model array: %s; report: %s\n' "$RG_RUN" "$prep" "$array" "$summary"
