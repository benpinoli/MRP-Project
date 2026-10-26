"""Run from repository root; Slurm supplies the frozen module on PYTHONPATH."""
import argparse
import json
import sys
from pathlib import Path

if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
    from samsung_research.regressions import collect, fit_task, freeze, prepare, read_json, readiness, tasks

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("stage", choices=["readiness", "freeze", "prepare", "fit", "collect", "count"])
    parser.add_argument("--repo", type=Path, default=Path.cwd())
    parser.add_argument("--config", type=Path, default=Path("configs/samsung_regressions.json"))
    parser.add_argument("--run", type=Path)
    parser.add_argument("--task", type=int)
    args = parser.parse_args()
    config = read_json(args.config)
    if args.stage == "readiness":
        print(json.dumps(readiness(args.repo, config), indent=2))
    elif args.stage == "count":
        print(len(tasks(config)))
    else:
        if args.run is None:
            parser.error("--run is required")
        if args.stage == "freeze":
            freeze(args.repo, args.run, args.config)
        elif args.stage == "prepare":
            prepare(args.repo, args.run, config)
        elif args.stage == "fit":
            if args.task is None or not 0 <= args.task < len(tasks(config)):
                parser.error("--task must identify an existing task")
            fit_task(args.run, args.task, config)
        else:
            counts = collect(args.run)
            print(json.dumps(counts))
            if counts["failed"] or counts["missing"]:
                sys.exit(1)
