"""Plot the cumulative log return of the Barra Leverage factor."""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import math
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import polars as pl


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

FACTOR = "USSLOWL_LEVERAGE"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--start", type=dt.date.fromisoformat, default=dt.date(1990, 1, 1))
    parser.add_argument("--end", type=dt.date.fromisoformat, default=dt.date(2026, 12, 31))
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("runs/factor_charts/leverage_1990_2026"),
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.end < args.start:
        raise ValueError("--end must be on or after --start")

    from sf_quant.data import load_factors

    raw = load_factors(args.start, args.end, [FACTOR]).sort("date")
    if raw.is_empty():
        raise ValueError("The factor query returned no rows")
    if raw["date"].n_unique() != raw.height:
        raise ValueError("The factor query contains duplicate dates")
    if raw[FACTOR].null_count():
        raise ValueError("The Leverage factor contains missing returns")

    returns_percent = raw[FACTOR].to_list()
    if any(not math.isfinite(value) for value in returns_percent):
        raise ValueError("The Leverage factor contains non-finite returns")
    if any(value <= -100 for value in returns_percent):
        raise ValueError("A return is at or below -100%; log1p is undefined")

    series = raw.with_columns(
        (pl.col(FACTOR) / 100).log1p().alias("log_return")
    ).with_columns(
        (pl.col("log_return").cum_sum() * 100).alias("cumulative_log_return_percent")
    )

    output_dir = args.output_dir.resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    chart_path = output_dir / "leverage_cumulative_log_return.png"
    series_path = output_dir / "leverage_cumulative_log_return.csv"
    metadata_path = output_dir / "metadata.json"

    series.write_csv(series_path)

    dates = series["date"].to_list()
    cumulative = series["cumulative_log_return_percent"].to_list()
    first_date = dates[0]
    last_date = dates[-1]

    plt.style.use("seaborn-v0_8-whitegrid")
    fig, ax = plt.subplots(figsize=(12, 6.75))
    ax.plot(dates, cumulative, color="#1f5a85", linewidth=1.45)
    ax.axhline(0, color="#333333", linewidth=0.8, alpha=0.65)
    ax.set_xlim(args.start, args.end)
    if first_date > args.start:
        ax.axvspan(args.start, first_date, color="#dddddd", alpha=0.45, linewidth=0)
        ax.text(
            args.start + (first_date - args.start) / 2,
            0.5,
            f"No source observations\nbefore {first_date:%Y-%m-%d}",
            transform=ax.get_xaxis_transform(),
            ha="center",
            va="center",
            fontsize=9,
            color="#666666",
        )
    fig.suptitle(
        "Leverage Factor — Cumulative Log Return",
        x=0.07,
        y=0.97,
        ha="left",
        fontsize=16,
        weight="bold",
    )
    fig.text(
        0.07,
        0.925,
        f"{first_date:%Y-%m-%d} to {last_date:%Y-%m-%d} | USSLOWL_LEVERAGE",
        fontsize=10,
        color="#555555",
    )
    ax.set_xlabel("")
    ax.set_ylabel("Cumulative log return (%)")
    ax.margins(x=0)
    ax.spines[["top", "right"]].set_visible(False)
    fig.text(
        0.01,
        0.01,
        "Daily vendor factor returns are converted from percent to decimal; cumulative series = 100 × Σ ln(1 + r_t).",
        fontsize=8.5,
        color="#555555",
    )
    fig.tight_layout(rect=(0, 0.04, 1, 0.9))
    fig.savefig(chart_path, dpi=200, bbox_inches="tight")
    plt.close(fig)

    metadata = {
        "factor": FACTOR,
        "requested_start": str(args.start),
        "requested_end": str(args.end),
        "actual_start": str(first_date),
        "actual_end": str(last_date),
        "coverage_note": (
            f"No source observations are available from {args.start} through "
            f"{first_date - dt.timedelta(days=1)}; no values were backfilled."
            if first_date > args.start
            else "The source covers the requested start date."
        ),
        "observations": series.height,
        "source": "sf_quant.data.load_factors",
        "source_units": "percent",
        "plotted_measure": "cumulative natural log return in percent",
        "formula": "100 * cumulative_sum(ln(1 + factor_return_percent / 100))",
        "ending_cumulative_log_return_percent": cumulative[-1],
        "series_file": series_path.name,
        "series_sha256": sha256(series_path),
        "chart_file": chart_path.name,
        "chart_sha256": sha256(chart_path),
    }
    metadata_path.write_text(json.dumps(metadata, indent=2) + "\n", encoding="utf-8")

    print(json.dumps(metadata, indent=2))


if __name__ == "__main__":
    main()
