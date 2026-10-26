"""Cluster-side sf-quant export only. Never infer geography, units or timing."""
import argparse
import datetime as dt
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--start", required=True, type=dt.date.fromisoformat)
    p.add_argument("--end", required=True, type=dt.date.fromisoformat)
    p.add_argument("--output", required=True, type=Path)
    p.add_argument("--config", type=Path, default=Path("configs/samsung_regressions.json"))
    args = p.parse_args()
    from sf_quant.data import load_factors
    from samsung_research.regressions import digest

    if args.output.exists() or args.output.with_suffix(args.output.suffix + ".metadata.json").exists():
        p.error("Export path already exists; choose a new immutable snapshot")
    names = json.loads(args.config.read_text())["factor_names"]
    df = load_factors(start=args.start, end=args.end, factors=names)
    if df.is_empty() or df["date"].n_unique() != df.height:
        raise ValueError("Empty or duplicate-date factor export")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    # Exclusive creation guards against accidental overwrite.
    with args.output.open("x", encoding="utf-8", newline="") as stream:
        df.sort("date").write_csv(stream)
    args.output.with_suffix(args.output.suffix + ".metadata.json").write_text(json.dumps(dict(
        exported_utc=dt.datetime.now(dt.timezone.utc).isoformat(), requested_start=str(args.start),
        requested_end=str(args.end), rows=df.height, columns=df.columns,
        sha256=digest(args.output), source="sf_quant.data.load_factors; local source version 0.2.7",
        model_geography_units_timing="Not verified by this export; complete separate metadata"), indent=2) + "\n")


if __name__ == "__main__":
    main()
