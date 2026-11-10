#!/usr/bin/env python3
"""Resolve candidate core-pair securities in the Silver Fund assets table."""
from __future__ import annotations

import argparse
from pathlib import Path

import polars as pl


NEEDLES = (
    "SK SQUARE",
    "SK HYNIX",
    "SAMSUNG FIRE",
    "SAMSUNG ELECTRONICS",
    "TAIWAN SEMICONDUCTOR",
)
TICKERS = ("402340", "000660", "000810", "005930", "2330", "TSM")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--assets",
        default="/home/bpinoli/groups/grp_quant/database/research/assets/assets_2026.parquet",
    )
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    name = pl.col("name").fill_null("").str.to_uppercase()
    ticker = pl.col("ticker").fill_null("").str.to_uppercase()
    predicate = pl.any_horizontal([name.str.contains(n, literal=True) for n in NEEDLES])
    predicate |= pl.any_horizontal([ticker == t for t in TICKERS])
    columns = [
        "barrid",
        "name",
        "ticker",
        "instrument",
        "issuerid",
        "iso_country_code",
        "iso_currency_code",
        "currency",
        "rootid",
    ]
    result = (
        pl.scan_parquet(args.assets)
        .filter(predicate)
        .select(columns)
        .unique()
        .sort(["name", "ticker", "barrid"])
        .collect()
    )
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    result.write_csv(output)
    print(result)
    print(f"wrote {result.height} identities to {output}")


if __name__ == "__main__":
    main()
