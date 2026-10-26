# Copy to slurm/cluster.env.sh (ignored), then edit on the school cluster.
# No hostname, account, module or filesystem path is guessed by this project.
export RESEARCH_REPO="/absolute/path/to/MRP-Project"
export RESEARCH_PYTHON="/absolute/path/to/venv/bin/python"
# Optional local cluster resources; omit if your cluster supplies defaults.
# export SLURM_ACCOUNT="your-allocation"
# export SLURM_PARTITION="your-cpu-partition"
export RG_CONCURRENCY=8
# Set ROOT and DATABASE privately only when using sf_quant's export adapter.
# Load site-required modules in your shell before submission.
