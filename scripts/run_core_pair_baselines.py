#!/usr/bin/env python3
"""Audit raw core-pair exports, build price panels, and estimate B00 baselines."""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from samsung_research.regressions import fit_ols  # noqa: E402


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def require(condition: bool, detail: str) -> None:
    if not condition:
        raise ValueError(detail)


def markdown_table(frame: pd.DataFrame) -> str:
    """Render a compact Markdown table without an optional tabulate dependency."""
    clean = frame.astype(object).where(frame.notna(), "").astype(str)
    header = "| " + " | ".join(clean.columns) + " |"
    rule = "| " + " | ".join(["---"] * len(clean.columns)) + " |"
    rows = ["| " + " | ".join(row.replace("|", "\\|") for row in values) + " |" for values in clean.to_numpy()]
    return "\n".join([header, rule, *rows])


def read_global(path: Path) -> pd.DataFrame:
    frame = pd.read_csv(path, dtype={"gvkey": str, "iid": str})
    frame["date"] = pd.to_datetime(frame["datadate"])
    require(not frame.duplicated(["gvkey", "iid", "date"]).any(), "duplicate Global security keys")
    return frame


def global_leg(raw: pd.DataFrame, spec: dict, prefix: str, required_prcstd: int) -> pd.DataFrame:
    x = raw[(raw.gvkey == spec["gvkey"]) & (raw.iid == spec["iid"])].copy().sort_values("date")
    require(len(x) > 0, f"no rows for {prefix}")
    require(x.conm.dropna().unique().tolist() == [spec["name"]], f"name mismatch for {prefix}")
    require(x.curcdd.dropna().unique().tolist() == [spec["currency"]], f"currency mismatch for {prefix}")
    price = pd.to_numeric(x.prccd, errors="coerce")
    adjustment = pd.to_numeric(x.ajexdi, errors="coerce")
    quote_unit = pd.to_numeric(x.qunit, errors="coerce")
    x[f"{prefix}_raw_close"] = price
    x[f"{prefix}_adjustment_factor"] = adjustment
    x[f"{prefix}_adjusted_close"] = price / adjustment / quote_unit
    x[f"{prefix}_volume"] = pd.to_numeric(x.cshtrd, errors="coerce")
    x[f"{prefix}_prcstd"] = pd.to_numeric(x.prcstd, errors="coerce")
    x[f"{prefix}_usable"] = (
        x[f"{prefix}_prcstd"].eq(required_prcstd)
        & x[f"{prefix}_adjusted_close"].gt(0)
        & adjustment.gt(0)
        & quote_unit.gt(0)
    )
    columns = ["date"] + [c for c in x.columns if c.startswith(prefix + "_")]
    return x[columns].reset_index(drop=True)


def read_fred(path: Path, value: str) -> pd.DataFrame:
    x = pd.read_csv(path, na_values=["."])
    x["date"] = pd.to_datetime(x.observation_date)
    x[value] = pd.to_numeric(x[value], errors="coerce")
    require(not x.date.duplicated().any(), f"duplicate FRED dates in {path.name}")
    require(x[value].dropna().gt(0).all(), f"nonpositive FRED values in {path.name}")
    return x[["date", value]]


def read_adr(paths: dict[str, Path]) -> tuple[pd.DataFrame, dict]:
    old = pd.read_csv(paths["adr_crsp_2005_2025"], dtype={"PERMNO": str})
    new = pd.read_csv(paths["adr_crsp_2026"], dtype={"PERMNO": str})
    na = pd.read_csv(paths["adr_compustat_na_2026"], dtype={"gvkey": str, "iid": str})
    for x in (old, new):
        require(x.PERMNO.eq("85442").all(), "unexpected CRSP PERMNO")
        x["date"] = pd.to_datetime(x.DlyCalDt)
    duplicate_rows = old.duplicated("date", keep=False)
    require(old.loc[duplicate_rows].duplicated(keep=False).all(), "non-identical duplicate CRSP rows")
    old_duplicate_dates = int(old.loc[duplicate_rows, "date"].nunique())
    old = old.drop_duplicates().copy()
    require(not old.date.duplicated().any(), "CRSP dates remain duplicated")
    require(new.date.max() == pd.Timestamp("2026-09-30"), "2026 CRSP cutoff changed")

    na["date"] = pd.to_datetime(na.datadate)
    require(na.gvkey.eq("201395").all() and na.iid.eq("90").all(), "unexpected NA GVKEY/IID")
    overlap = new.merge(na, on="date", how="inner", validate="one_to_one", suffixes=("_crsp", "_na"))
    overlap = overlap[overlap.date <= pd.Timestamp("2026-09-30")].copy()
    exact = pd.to_numeric(overlap.DlyPrc).to_numpy() == pd.to_numeric(overlap.prccd).to_numpy()
    require(len(overlap) == 5 and bool(exact.all()), "ADR five-close overlap no longer matches exactly")

    def crsp_rows(x: pd.DataFrame, source: str) -> pd.DataFrame:
        out = pd.DataFrame({
            "date": x.date,
            "adr_raw_close": pd.to_numeric(x.DlyPrc, errors="coerce").abs(),
            "adr_adjustment_factor": pd.to_numeric(x.DlyCumFacPr, errors="coerce"),
            "adr_volume": pd.to_numeric(x.DlyVol, errors="coerce"),
            "adr_return": pd.to_numeric(x.DlyRet, errors="coerce"),
            "adr_bid": pd.to_numeric(x.DlyBid, errors="coerce"),
            "adr_ask": pd.to_numeric(x.DlyAsk, errors="coerce"),
            "adr_source": source,
        })
        out["adr_adjusted_close"] = out.adr_raw_close / out.adr_adjustment_factor
        out["adr_usable"] = out.adr_adjusted_close.gt(0) & out.adr_adjustment_factor.gt(0)
        return out

    pieces = [
        crsp_rows(old, "crsp_2005_2025"),
        crsp_rows(new, "crsp_2026_through_2026-09-30"),
    ]
    na_use = na[na.date.between("2026-10-01", "2026-11-06")].copy()
    na_out = pd.DataFrame({
        "date": na_use.date,
        "adr_raw_close": pd.to_numeric(na_use.prccd, errors="coerce"),
        "adr_adjustment_factor": pd.to_numeric(na_use.ajexdi, errors="coerce"),
        "adr_volume": pd.to_numeric(na_use.cshtrd, errors="coerce"),
        "adr_return": np.nan,
        "adr_bid": np.nan,
        "adr_ask": np.nan,
        "adr_source": "compustat_na_2026-10-01_through_2026-11-06",
    })
    na_out["adr_adjusted_close"] = na_out.adr_raw_close / na_out.adr_adjustment_factor
    na_out["adr_usable"] = na_out.adr_adjusted_close.gt(0) & na_out.adr_adjustment_factor.gt(0)
    pieces.append(na_out)
    adr = pd.concat(pieces, ignore_index=True).sort_values("date").reset_index(drop=True)
    require(not adr.date.duplicated().any(), "stitched ADR dates overlap")
    audit = {
        "old_crsp_exact_duplicate_dates_dropped": old_duplicate_dates,
        "overlap_dates": overlap.date.dt.strftime("%Y-%m-%d").tolist(),
        "overlap_exact_numeric_close_matches": int(exact.sum()),
        "crsp_last_date": new.date.max().strftime("%Y-%m-%d"),
        "compustat_na_first_used_date": na_out.date.min().strftime("%Y-%m-%d"),
        "compustat_na_unavailable_crsp_fields_left_missing": ["adr_return", "adr_bid", "adr_ask"],
    }
    return adr, audit


def add_changes(panel: pd.DataFrame, usable: pd.Series, gap: pd.Series, log_gap: pd.Series) -> pd.DataFrame:
    panel["gap_pct"] = gap.where(usable)
    panel["log_gap"] = log_gap.where(usable)
    adjacent = usable & usable.shift(fill_value=False)
    panel["dd_pp"] = panel.gap_pct.diff().where(adjacent)
    panel["dg"] = panel.log_gap.diff().where(adjacent)
    panel["lag_gap"] = panel.gap_pct.shift().where(adjacent)
    panel["usable_level"] = usable
    panel["usable_change"] = adjacent
    panel["grid_index"] = np.arange(len(panel))
    return panel


def normalized_pair(raw: pd.DataFrame, spec: dict, required: int) -> tuple[pd.DataFrame, dict]:
    left = global_leg(raw, spec["left"], "left", required)
    right = global_leg(raw, spec["right"], "right", required)
    panel = left.merge(right, on="date", how="outer", validate="one_to_one", indicator="_join").sort_values("date").reset_index(drop=True)
    usable = panel.left_usable.eq(True) & panel.right_usable.eq(True)
    ratio = panel.left_adjusted_close / panel.right_adjusted_close
    anchor_date = panel.loc[usable, "date"].iloc[0]
    anchor = float(ratio[usable].iloc[0])
    panel["price_ratio"] = ratio
    panel = add_changes(panel, usable, 100 * (1 - ratio / anchor), np.log(anchor / ratio))
    audit = {
        "pair": spec["id"],
        "left_rows": int(len(left)), "right_rows": int(len(right)),
        "outer_union_rows": int(len(panel)), "both_security_dates": int(panel._join.eq("both").sum()),
        "left_only_dates": int(panel._join.eq("left_only").sum()), "right_only_dates": int(panel._join.eq("right_only").sum()),
        "usable_level_rows": int(usable.sum()), "usable_change_rows": int(panel.usable_change.sum()),
        "anchor_date": anchor_date.strftime("%Y-%m-%d"), "anchor_adjusted_price_ratio": anchor,
        "first_usable_date": panel.loc[usable, "date"].min().strftime("%Y-%m-%d"),
        "last_usable_date": panel.loc[usable, "date"].max().strftime("%Y-%m-%d"),
    }
    panel["pair"] = spec["id"]
    return panel.drop(columns="_join"), audit


def tsmc_pair(raw: pd.DataFrame, adr: pd.DataFrame, fx: pd.DataFrame, spec: dict, required: int) -> tuple[pd.DataFrame, dict]:
    local = global_leg(raw, spec["local"], "local", required)
    panel = local.merge(adr, on="date", how="outer", validate="one_to_one", indicator="_security_join").sort_values("date").reset_index(drop=True)
    panel = panel.merge(fx, on="date", how="left", validate="one_to_one")
    # Latest fixing strictly before the local calendar date is a transparent timing sensitivity.
    prior = fx.dropna(subset=["DEXTAUS"]).sort_values("date").rename(columns={"date": "prior_fx_date", "DEXTAUS": "DEXTAUS_prior"})
    panel = pd.merge_asof(panel.sort_values("date"), prior, left_on="date", right_on="prior_fx_date", direction="backward", allow_exact_matches=False)
    usable = panel.local_usable.eq(True) & panel.adr_usable.eq(True) & panel.DEXTAUS.gt(0)
    local_ads_usd = spec["common_shares_per_ads"] * panel.local_adjusted_close / panel.DEXTAUS
    ratio = panel.adr_adjusted_close / local_ads_usd
    panel["local_ads_usd_same_day_noon_fx"] = local_ads_usd
    panel["local_ads_usd_prior_fixing"] = spec["common_shares_per_ads"] * panel.local_adjusted_close / panel.DEXTAUS_prior
    panel["price_ratio"] = ratio
    panel["gap_pct_prior_fx"] = 100 * (panel.adr_adjusted_close / panel.local_ads_usd_prior_fixing - 1)
    panel = add_changes(panel, usable, 100 * (ratio - 1), np.log(ratio))
    audit = {
        "pair": spec["id"],
        "local_rows": int(len(local)), "adr_rows": int(len(adr)),
        "outer_union_rows": int(len(panel)), "both_security_dates": int(panel._security_join.eq("both").sum()),
        "local_only_dates": int(panel._security_join.eq("left_only").sum()), "adr_only_dates": int(panel._security_join.eq("right_only").sum()),
        "both_security_dates_missing_same_day_fx": int((panel._security_join.eq("both") & panel.DEXTAUS.isna()).sum()),
        "usable_level_rows": int(usable.sum()), "usable_change_rows": int(panel.usable_change.sum()),
        "first_usable_date": panel.loc[usable, "date"].min().strftime("%Y-%m-%d"),
        "last_usable_date": panel.loc[usable, "date"].max().strftime("%Y-%m-%d"),
        "common_shares_per_ads": spec["common_shares_per_ads"],
        "baseline_fx_timing": "same-calendar-date FRED DEXTAUS noon New York fixing; after Taiwan close and therefore retrospective",
        "timing_sensitivity": "gap_pct_prior_fx uses latest fixing strictly before the Taiwan calendar date",
    }
    panel["pair"] = spec["id"]
    return panel.drop(columns="_security_join"), audit


def fit_baselines(panels: pd.DataFrame, cfg: dict) -> tuple[pd.DataFrame, pd.DataFrame]:
    coefficients: list[dict] = []
    statuses: list[dict] = []
    dates = pd.to_datetime(panels.date)
    for pair in [x["id"] for x in cfg["pairs"]]:
        for window in cfg["windows"]:
            mask = panels.pair.eq(pair) & dates.between(window["start"], window["end"])
            sample = panels.loc[mask].dropna(subset=["dd_pp", "lag_gap"])
            for hac in cfg["hac_lags"]:
                base = {"pair": pair, "model": "B00", "window": window["id"], "hac_lag": hac}
                try:
                    x = np.column_stack([np.ones(len(sample)), sample.lag_gap.to_numpy(float)])
                    b, se, p, _, diag = fit_ols(sample.dd_pp, x, sample.grid_index, hac, minimum=cfg["minimum_observations"])
                except ValueError as exc:
                    statuses.append({**base, "status": "blocked", "detail": str(exc), "n": int(len(sample)),
                                     "sample_start": sample.date.min() if len(sample) else "", "sample_end": sample.date.max() if len(sample) else ""})
                    continue
                for term, i in (("intercept", 0), ("lag_gap", 1)):
                    coefficients.append({**base, "term": term, "coefficient": b[i], "standard_error": se[i], "p_value": p[i],
                                         "n": diag["n"], "adjusted_r2": diag["adjusted_r_squared"]})
                statuses.append({**base, "status": "estimated", "detail": "", "n": diag["n"],
                                 "sample_start": sample.date.min(), "sample_end": sample.date.max(),
                                 "adjusted_r2": diag["adjusted_r_squared"], "condition_number": diag["standardized_condition"]})
    return pd.DataFrame(coefficients), pd.DataFrame(statuses)


def identifier_audit(paths: dict[str, Path], cfg: dict) -> pd.DataFrame:
    company = pd.read_csv(paths["global_company"], dtype=str)
    security = pd.read_csv(paths["global_security"], dtype=str)
    history = pd.read_csv(paths["global_security_history"], dtype=str)
    rows = []
    for pair in cfg["pairs"]:
        for role in ("left", "right", "local"):
            if role not in pair:
                continue
            s = pair[role]
            c = company[company.gvkey.eq(s["gvkey"])]
            q = security[security.gvkey.eq(s["gvkey"]) & security.iid.eq(s["iid"])]
            h = history[history.gvkey.eq(s["gvkey"]) & history.iid.eq(s["iid"])]
            require(len(c) == 1 and len(q) == 1, f"descriptor identity missing for {s}")
            rows.append({"pair": pair["id"], "role": role, "vendor": "Compustat Global", "primary_id": s["gvkey"],
                         "secondary_id": s["iid"], "name": c.conm.iloc[0], "security_id": q['isin'].iloc[0],
                         "country": q.excntry.iloc[0], "active": q.secstat.iloc[0],
                         "history_items": ";".join(sorted(h.item.astype(str).unique()))})
    names = pd.read_csv(paths["adr_crsp_names"], dtype={"permno": str})
    require(names.permno.eq("85442").all() and names.ticker.eq("TSM").all(), "CRSP name history mismatch")
    rows.append({"pair": "tsmc_local_adr", "role": "adr", "vendor": "CRSP", "primary_id": "85442",
                 "secondary_id": names.permco.iloc[-1], "name": names.issuernm.iloc[-1], "security_id": names.cusip.iloc[-1],
                 "country": "US-listed ADR", "active": names.tradingstatusflg.iloc[-1],
                 "history_items": f"{len(names)} name-history rows; {names.secinfostartdt.min()} through {names.secinfoenddt.max()}"})
    return pd.DataFrame(rows)


def fundamentals_audit(paths: dict[str, Path]) -> pd.DataFrame:
    rows = []
    for frequency, key, fdate, pdate in (
        ("annual", "fundamentals_annual", "fdate", "pdate"),
        ("quarterly", "fundamentals_quarterly", "fdateq", "pdateq"),
    ):
        x = pd.read_csv(paths[key], dtype={"gvkey": str})
        x["datadate"] = pd.to_datetime(x.datadate)
        for col in (fdate, pdate):
            x[col] = pd.to_datetime(x[col], errors="coerce")
        require(not x.duplicated(["gvkey", "datadate", "indfmt"]).any(), f"duplicate {frequency} fundamentals")
        for gvkey, g in x.groupby("gvkey"):
            rows.append({"frequency": frequency, "gvkey": gvkey, "name": g.conm.iloc[0], "rows": len(g),
                         "period_start": g.datadate.min().strftime("%Y-%m-%d"), "period_end": g.datadate.max().strftime("%Y-%m-%d"),
                         "fdate_present": int(g[fdate].notna().sum()), "fdate_missing": int(g[fdate].isna().sum()),
                         "pdate_present": int(g[pdate].notna().sum()), "pdate_missing": int(g[pdate].isna().sum()),
                         "first_pdate": g[pdate].min().strftime("%Y-%m-%d") if g[pdate].notna().any() else "",
                         "last_pdate": g[pdate].max().strftime("%Y-%m-%d") if g[pdate].notna().any() else "",
                         "publication_clock_status": "vendor fdate/pdate fields present; original public-release timestamp and revision vintage not established"})
    return pd.DataFrame(rows)


def render_report(audits: list[dict], statuses: pd.DataFrame, adr_audit: dict, fundamentals: pd.DataFrame) -> str:
    primary = statuses[(statuses.hac_lag == 20) & (statuses.window == "full")]
    lines = [
        "# Remaining core-pair price baselines", "",
        "These are retrospective price-gap baselines, not NAV discounts, fair values, causal estimates, forecasts, or trading tests.", "",
        "## Coverage and joins", "", markdown_table(pd.DataFrame(audits)), "",
        "## Full-window B00 status (HAC 20)", "", markdown_table(primary), "",
        "## ADR handoff", "", f"The five overlapping closes ({', '.join(adr_audit['overlap_dates'])}) matched exactly numerically.",
        "Rows through 2026-09-30 use CRSP; rows from 2026-10-01 through 2026-11-06 use Compustat North America and are source-tagged. CRSP-only return/bid/ask fields remain missing after the handoff.", "",
        "## Timing and adjustments", "",
        "Compustat closes are divided by AJEXDI and QUNIT; CRSP closes are divided by DlyCumFacPr. This neutralizes the Samsung Electronics 50:1 split and TSMC share distributions instead of treating them as gap changes. No dividend total-return adjustment is used.",
        "Korean pair outcomes use same-currency KRW ratios, so DEXKOUS is audited but not needed algebraically. TSMC converts five Taiwan common shares per ADS using same-calendar-date DEXTAUS (TWD per USD). That FRED observation is a noon New York fixing after the Taiwan close, so the baseline is retrospective; `gap_pct_prior_fx` preserves a prior-fixing timing sensitivity.", "",
        "## Fundamentals publication-date audit", "", markdown_table(fundamentals), "",
        "Annual and quarterly fundamentals are audited separately and are not used in these price regressions. Dated ownership histories remain insufficient for both Korean pairs, so Korean NAV regressions remain pending.", "",
        "## Provenance gaps", "",
        "The upload includes SQL for quarterly fundamentals and the Compustat North America ADR handoff. It does not include the original WRDS query for the Global daily export, annual fundamentals, CRSP 2005-2025, CRSP 2026, CRSP name history, or Global descriptor exports. The CRSP 2026 query-summary PDF is retained but is not an executable query. FRED retrieval metadata/vintage files are also absent. CRSP name history supplied here ends 2025-12-31; the 2026 CRSP daily export's embedded security fields support the 2026 continuation.", "",
        "The ownership observation in commit `3666efa` is one SK Square/SK Hynix point (146.1 million shares at 2021-12-31, filed 2022-02-24), not a dated history. The two Korean filing PDFs are individual observations only.", "",
    ]
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="configs/core_pair_baselines.v1.json")
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    config_path = ROOT / args.config
    cfg = json.loads(config_path.read_text(encoding="utf-8"))
    raw_dir = ROOT / cfg["raw_dir"]
    paths = {k: raw_dir / v for k, v in cfg["inputs"].items()}
    missing = [str(p) for p in paths.values() if not p.is_file()]
    if missing:
        raise FileNotFoundError(missing)
    before = {p.name: digest(p) for p in sorted(raw_dir.iterdir()) if p.is_file()}

    raw = read_global(paths["global_daily"])
    fx_twd = read_fred(paths["fred_twd"], "DEXTAUS")
    fx_krw = read_fred(paths["fred_krw"], "DEXKOUS")
    adr, adr_audit = read_adr(paths)
    panels, audits = [], []
    for spec in cfg["pairs"]:
        if spec["construction"] == "normalized_ratio":
            panel, audit = normalized_pair(raw, spec, cfg["sample"]["required_prcstd"])
        else:
            panel, audit = tsmc_pair(raw, adr, fx_twd, spec, cfg["sample"]["required_prcstd"])
        panel = panel[panel.date.between(cfg["sample"]["start"], cfg["sample"]["end"])].copy()
        panels.append(panel); audits.append(audit)
    combined = pd.concat(panels, ignore_index=True, sort=False)
    coefficients, statuses = fit_baselines(combined, cfg)
    identifiers = identifier_audit(paths, cfg)
    fundamentals = fundamentals_audit(paths)

    output = ROOT / args.output
    output.mkdir(parents=True, exist_ok=False)
    combined.to_csv(output / "panels.csv", index=False)
    coefficients.to_csv(output / "coefficients.csv", index=False)
    statuses.to_csv(output / "model_status.csv", index=False)
    pd.DataFrame(audits).to_csv(output / "coverage_join_audit.csv", index=False)
    identifiers.to_csv(output / "identifier_matches.csv", index=False)
    fundamentals.to_csv(output / "fundamentals_coverage.csv", index=False)
    after = {p.name: digest(p) for p in sorted(raw_dir.iterdir()) if p.is_file()}
    require(before == after, "raw input bytes changed during run")
    manifest = {
        "config": str(config_path.relative_to(ROOT)), "config_sha256": digest(config_path),
        "raw_files_sha256_before_and_after": before, "raw_bytes_preserved": True,
        "fred_krw_rows_audited_not_used_in_same_currency_ratios": len(fx_krw),
        "adr_handoff": adr_audit, "coverage": audits,
        "estimated_models": int(statuses.status.eq("estimated").sum()), "blocked_models": int(statuses.status.eq("blocked").sum()),
    }
    (output / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    (output / "REPORT.md").write_text(render_report(audits, statuses, adr_audit, fundamentals), encoding="utf-8")
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
