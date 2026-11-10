#!/usr/bin/env python3
"""Run frozen descriptive Prosus/Tencent/Naspers return regressions.

The primary series is a USD close-to-close *price* return. It is deliberately
not labelled a certified total return: WRDS AJEXDI/TRFD definitions were not
packaged, while the Yahoo adjusted series changes regime around Tencent's
in-specie distributions. No NAV, forecasting, or trading calculation appears
here.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import platform
import sys
import zipfile
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statsmodels.api as sm
from statsmodels.stats.diagnostic import acorr_ljungbox, het_breuschpagan
from statsmodels.stats.outliers_influence import variance_inflation_factor
from statsmodels.stats.stattools import durbin_watson, jarque_bera


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONFIG = ROOT / "configs/prosus_tencent_return_regressions.v1.json"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def read_config(path: Path) -> dict:
    cfg = json.loads(path.read_text(encoding="utf-8"))
    assert cfg["schema_version"] == 1
    assert list(cfg["designs"]) == ["A", "B", "C"]
    assert set(cfg["designs"]["A"]).issubset(cfg["designs"]["B"])
    assert set(cfg["designs"]["B"]).issubset(cfg["designs"]["C"])
    return cfg


def verify_bundle_integrity(bundle: Path) -> dict:
    """Recheck transfer integrity without modifying the extracted bundle."""
    archive = ROOT / "data/prosus_tencent_validated_2026-11-02.zip"
    checksum_file = archive.with_suffix(archive.suffix + ".sha256")
    expected_archive_sha = checksum_file.read_text(encoding="utf-8").split()[0]
    manifest_path = bundle / "logs/package_manifest.json"
    records = json.loads(manifest_path.read_text(encoding="utf-8"))["files"]
    failures = []
    for record in records:
        path = bundle / record["path"]
        actual_sha = sha256(path) if path.is_file() else None
        actual_bytes = path.stat().st_size if path.is_file() else None
        if actual_sha != record["sha256"] or actual_bytes != record["bytes"]:
            failures.append({"path": record["path"], "expected_sha256": record["sha256"], "actual_sha256": actual_sha, "expected_bytes": record["bytes"], "actual_bytes": actual_bytes})
    with zipfile.ZipFile(archive) as zf:
        members = zf.infolist()
        unsafe = [m.filename for m in members if PurePosixPath(m.filename).is_absolute() or ".." in PurePosixPath(m.filename).parts or "\\" in m.filename]
        bad_crc_member = zf.testzip()
    result = {
        "archive": str(archive.relative_to(ROOT)), "expected_bytes": 32862935, "actual_bytes": archive.stat().st_size,
        "expected_sha256": expected_archive_sha, "actual_sha256": sha256(archive),
        "expected_zip_member_count": 130, "zip_member_count": len(members), "unsafe_member_paths": unsafe,
        "bad_crc_member": bad_crc_member, "manifest_path": str(manifest_path.relative_to(ROOT)),
        "manifest_entries": len(records), "manifest_failures": failures, "all_manifest_files_passed": not failures,
    }
    result["passed"] = result["actual_bytes"] == result["expected_bytes"] and result["actual_sha256"] == result["expected_sha256"] and result["zip_member_count"] == result["expected_zip_member_count"] and not unsafe and bad_crc_member is None and not failures
    if not result["passed"]:
        raise ValueError(f"bundle integrity failed: {result}")
    return result


def exact_fx_panel(bundle: Path) -> pd.DataFrame:
    fx = pd.read_csv(bundle / "data/raw/ecb_fx_daily_long.csv", parse_dates=["date"])
    wide = fx.pivot(index="date", columns="currency", values="foreign_units_per_EUR")
    wide["EUR"] = 1.0
    if not (wide > 0).all().all():
        raise ValueError("ECB FX contains nonpositive or missing observed rates")
    return wide.sort_index()


def usd_value(local_value: pd.Series, currency: str, dates: pd.Series, fx: pd.DataFrame) -> pd.Series:
    """Convert using ECB foreign units/EUR: local/local-per-EUR * USD-per-EUR."""
    idx = pd.DatetimeIndex(dates)
    local_per_eur = fx[currency].reindex(idx).to_numpy()
    usd_per_eur = fx["USD"].reindex(idx).to_numpy()
    return pd.Series(local_value.to_numpy() / local_per_eur * usd_per_eur, index=local_value.index)


def security_returns(bundle: Path, cfg: dict, fx: pd.DataFrame) -> tuple[dict[str, pd.DataFrame], pd.DataFrame, dict]:
    src = bundle / "data/processed/wrds_security_daily_research.csv"
    raw = pd.read_csv(src, dtype={"gvkey": str, "iid": str}, parse_dates=["datadate"])
    outputs: dict[str, pd.DataFrame] = {}
    audit_rows: list[pd.DataFrame] = []
    identity_audit = {}
    for key, spec in cfg["securities"].items():
        g = raw[(raw.gvkey == spec["gvkey"]) & (raw.iid == spec["iid"])].copy()
        g = g.sort_values("datadate").reset_index(drop=True)
        observed = {
            "rows": int(len(g)), "issuer": sorted(g.conm.dropna().unique().tolist()),
            "currency": sorted(g.curcdd.dropna().unique().tolist()),
            "exchange": sorted(pd.to_numeric(g.exchg, errors="coerce").dropna().astype(int).unique().tolist()),
            "isin": sorted(g["isin"].dropna().unique().tolist()),
            "qunit": sorted(pd.to_numeric(g.qunit, errors="coerce").dropna().unique().tolist()),
            "prcstd_counts": {str(k): int(v) for k, v in g.prcstd.value_counts().sort_index().items()},
        }
        identity_audit[key] = observed
        if observed["issuer"] != [spec["issuer"]] or observed["currency"] != [spec["currency"]] or observed["exchange"] != [spec["exchange"]]:
            raise ValueError(f"identity audit failed for {key}: {observed}")
        g["start_date"] = g.datadate.shift(1)
        g["end_date"] = g.datadate
        g["previous_prcstd"] = g.prcstd.shift(1)
        g["previous_ajexdi"] = g.ajexdi.shift(1)
        g["previous_split"] = g.split.shift(1)
        g["previous_splitf"] = g.splitf.shift(1)
        g["local_price"] = g.prccd / g.qunit
        g["usd_price"] = usd_value(g.local_price, spec["currency"], g.end_date, fx)
        g["previous_usd_price"] = g.usd_price.shift(1)
        g["fx_current_exact"] = g.end_date.isin(fx.index)
        g["fx_previous_exact"] = g.start_date.isin(fx.index)
        g["price_flags_usable"] = g.prcstd.eq(cfg["sample"]["require_prcstd"]) & g.previous_prcstd.eq(cfg["sample"]["require_prcstd"])
        g["adjustment_unchanged"] = g.ajexdi.eq(g.previous_ajexdi)
        split_cols = ["split", "splitf", "previous_split", "previous_splitf"]
        g["no_split_marker"] = g[split_cols].fillna(0).eq(0).all(axis=1)
        g["positive_prices"] = g.usd_price.gt(0) & g.previous_usd_price.gt(0)
        usable = g.price_flags_usable & g.fx_current_exact & g.fx_previous_exact & g.positive_prices
        if cfg["sample"]["exclude_adjustment_factor_changes"]:
            usable &= g.adjustment_unchanged
        if cfg["sample"]["exclude_nonzero_split_fields"]:
            usable &= g.no_split_marker
        g["usable"] = usable
        g["return"] = np.where(usable, g.usd_price / g.previous_usd_price - 1.0, np.nan)
        reasons = np.select(
            [g.start_date.isna(), ~g.price_flags_usable, ~(g.fx_current_exact & g.fx_previous_exact), ~g.positive_prices, ~g.adjustment_unchanged, ~g.no_split_marker],
            ["no_previous_row", "prcstd_endpoint_not_10", "missing_exact_ecb_fx_endpoint", "nonpositive_or_missing_price", "ajexdi_changed", "split_marker"],
            default="included",
        )
        g["exclusion_reason"] = reasons
        g["security"] = key
        audit_rows.append(g[["security", "start_date", "end_date", "prcstd", "previous_prcstd", "ajexdi", "previous_ajexdi", "usable", "return", "exclusion_reason"]])
        outputs[key] = g.loc[g.usable, ["start_date", "end_date", "return"]].rename(columns={"return": f"{key}_return"})
    return outputs, pd.concat(audit_rows, ignore_index=True), identity_audit


def market_return(bundle: Path, dataset: str, currency: str, fx: pd.DataFrame, out_name: str) -> pd.DataFrame:
    g = pd.read_csv(bundle / f"data/raw/{dataset}.csv", parse_dates=["date"]).sort_values("date").reset_index(drop=True)
    g["start_date"] = g.date.shift(1)
    g["end_date"] = g.date
    g["usd_price"] = usd_value(g.close, currency, g.end_date, fx)
    exact = g.end_date.isin(fx.index) & g.start_date.isin(fx.index)
    g[out_name] = np.where(exact & g.usd_price.gt(0) & g.usd_price.shift(1).gt(0), g.usd_price / g.usd_price.shift(1) - 1.0, np.nan)
    return g.loc[g[out_name].notna(), ["start_date", "end_date", out_name]]


def factor_panel(bundle: Path, cfg: dict) -> tuple[pd.DataFrame, dict]:
    merged = None
    audit = {}
    rf_series = []
    for block, filename in cfg["factor_blocks"].items():
        f = pd.read_csv(bundle / "data/processed" / filename, parse_dates=["date"]).sort_values("date").reset_index(drop=True)
        f["start_date"] = f.date.shift(1)
        f["end_date"] = f.date
        ren = {col: f"{block}_{col}" for col in cfg["factor_columns"]}
        f = f.rename(columns=ren)
        rf_series.append(f[["start_date", "end_date", "RF"]].rename(columns={"RF": f"RF_{block}"}))
        keep = ["start_date", "end_date"] + list(ren.values())
        merged = f[keep] if merged is None else merged.merge(f[keep], on=["start_date", "end_date"], how="inner", validate="one_to_one")
        corr = f[list(ren.values())].corr()
        audit[block] = {"rows": int(len(f)), "first": str(f.end_date.min().date()), "last": str(f.end_date.max().date()), "max_abs_within_block_correlation": float((corr.abs() - np.eye(len(corr))).max().max())}
    rf = rf_series[0]
    for other in rf_series[1:]:
        rf = rf.merge(other, on=["start_date", "end_date"], validate="one_to_one")
    rf_cols = [c for c in rf if c.startswith("RF_")]
    audit["rf_max_abs_difference"] = float((rf[rf_cols].max(axis=1) - rf[rf_cols].min(axis=1)).abs().max())
    if audit["rf_max_abs_difference"] > 1e-12:
        raise ValueError("regional RF series differ; frozen single-RF convention is invalid")
    rf["RF"] = rf[rf_cols[0]]
    return merged.merge(rf[["start_date", "end_date", "RF"]], on=["start_date", "end_date"], validate="one_to_one"), audit


def build_relationship_samples(bundle: Path, cfg: dict) -> tuple[dict[str, pd.DataFrame], pd.DataFrame, dict]:
    fx = exact_fx_panel(bundle)
    stocks, exclusions, identity = security_returns(bundle, cfg, fx)
    euro = market_return(bundle, cfg["markets"]["europe"]["dataset"], "EUR", fx, "europe_market_usd_return")
    hk = market_return(bundle, cfg["markets"]["hong_kong"]["dataset"], "HKD", fx, "hong_kong_market_usd_return")
    factors, factor_audit = factor_panel(bundle, cfg)
    controls = euro.merge(hk, on=["start_date", "end_date"], how="inner", validate="one_to_one").merge(factors, on=["start_date", "end_date"], how="inner", validate="one_to_one")
    samples = {}
    attrition = {}
    for rel in cfg["relationships"]:
        rid, dep, exp = rel["id"], rel["dependent"], rel["explanatory"]
        pair = stocks[dep].merge(stocks[exp], on=["start_date", "end_date"], how="inner", validate="one_to_one")
        full = pair.merge(controls, on=["start_date", "end_date"], how="inner", validate="one_to_one")
        full = full[(full.end_date >= cfg["sample"]["start"]) & (full.end_date <= cfg["sample"]["end"])].copy()
        full["dependent_excess_return"] = full[f"{dep}_return"] - full.RF
        full["explanatory_excess_return"] = full[f"{exp}_return"] - full.RF
        required = ["dependent_excess_return"] + cfg["designs"]["C"]
        common = full.dropna(subset=required).sort_values("end_date").reset_index(drop=True)
        common["relationship"] = rid
        samples[rid] = common
        attrition[rid] = {
            "dependent_usable_intervals": int(len(stocks[dep])), "explanatory_usable_intervals": int(len(stocks[exp])),
            "exact_pair_intervals": int(len(pair)), "after_all_controls_and_date_bounds": int(len(full)),
            "common_model_sample": int(len(common)), "first_end_date": str(common.end_date.min().date()), "last_end_date": str(common.end_date.max().date()),
        }
    return samples, exclusions, {"identity": identity, "factors": factor_audit, "attrition": attrition}


def matrix_diagnostics(frame: pd.DataFrame, columns: list[str]) -> dict:
    x = sm.add_constant(frame[columns], has_constant="add")
    scaled = x.copy()
    for col in columns:
        std = scaled[col].std(ddof=0)
        scaled[col] = (scaled[col] - scaled[col].mean()) / std if std else scaled[col]
    condition = float(np.linalg.cond(scaled.to_numpy()))
    vif = {col: float(variance_inflation_factor(x.to_numpy(), i)) for i, col in enumerate(x.columns) if col != "const"}
    return {"condition_number_standardized": condition, "vif": vif, "max_vif": max(vif.values())}


def residual_diagnostics(result) -> dict:
    resid = result.resid
    jb, jbp, skew, kurt = jarque_bera(resid)
    bp_lm, bp_lmp, bp_f, bp_fp = het_breuschpagan(resid, result.model.exog)
    lags = [lag for lag in (5, 20) if lag < len(resid) // 5]
    lb = acorr_ljungbox(resid, lags=lags, return_df=True)
    return {
        "durbin_watson": float(durbin_watson(resid)), "jarque_bera": float(jb), "jarque_bera_pvalue": float(jbp),
        "skew": float(skew), "kurtosis": float(kurt), "breusch_pagan_lm": float(bp_lm), "breusch_pagan_pvalue": float(bp_lmp),
        **{f"ljung_box_pvalue_lag_{lag}": float(lb.loc[lag, "lb_pvalue"]) for lag in lags},
    }


def fit_one(frame: pd.DataFrame, columns: list[str], hac_lag: int):
    x = sm.add_constant(frame[columns], has_constant="add")
    return sm.OLS(frame.dependent_excess_return, x).fit(cov_type="HAC", cov_kwds={"maxlags": hac_lag, "use_correction": True})


def coefficient_rows(result, relationship: str, design: str, hac_lag: int, sample: str) -> list[dict]:
    ci = result.conf_int(alpha=.05)
    return [{
        "relationship": relationship, "sample": sample, "design": design, "hac_lag": hac_lag, "term": term,
        "coefficient": float(result.params[term]), "standard_error": float(result.bse[term]), "t_stat": float(result.tvalues[term]),
        "p_value": float(result.pvalues[term]), "ci_low": float(ci.loc[term, 0]), "ci_high": float(ci.loc[term, 1]),
        "n": int(result.nobs), "adjusted_r2": float(result.rsquared_adj), "r2": float(result.rsquared),
    } for term in result.params.index]


def fit_models(samples: dict[str, pd.DataFrame], cfg: dict, sample_label: str = "primary") -> tuple[pd.DataFrame, list[dict], list[dict]]:
    rows, model_rows, diagnostics = [], [], []
    for rid, frame in samples.items():
        fitted = {}
        for design, cols in cfg["designs"].items():
            for lag in [cfg["uncertainty"]["primary_hac_lag"], cfg["uncertainty"]["sensitivity_hac_lag"]]:
                result = fit_one(frame, cols, lag)
                rows.extend(coefficient_rows(result, rid, design, lag, sample_label))
                if lag == cfg["uncertainty"]["primary_hac_lag"]:
                    fitted[design] = result
                    diagnostics.append({"relationship": rid, "sample": sample_label, "design": design, **matrix_diagnostics(frame, cols), **residual_diagnostics(result)})
        for design, result in fitted.items():
            previous = {"B": "A", "C": "B"}.get(design)
            partial = None
            delta_adj = None
            if previous:
                reduced = fitted[previous]
                partial = float((reduced.ssr - result.ssr) / reduced.ssr)
                delta_adj = float(result.rsquared_adj - reduced.rsquared_adj)
            model_rows.append({"relationship": rid, "sample": sample_label, "design": design, "n": int(result.nobs), "r2": float(result.rsquared), "adjusted_r2": float(result.rsquared_adj), "partial_r2_vs_previous": partial, "adjusted_r2_change_vs_previous": delta_adj, "columns": cfg["designs"][design]})
    return pd.DataFrame(rows), model_rows, diagnostics


def action_window_samples(samples: dict[str, pd.DataFrame], cfg: dict) -> dict[str, pd.DataFrame]:
    days = cfg["sensitivities"]["corporate_action_window_calendar_days"]
    events = [(pd.Timestamp(e["date"]), e["entity"]) for e in cfg["sensitivities"]["events"]]
    rel_entities = {r["id"]: {r["dependent"], r["explanatory"]} for r in cfg["relationships"]}
    output = {}
    for rid, frame in samples.items():
        keep = pd.Series(True, index=frame.index)
        for date, entity in events:
            if entity in rel_entities[rid]:
                keep &= ~frame.end_date.between(date - pd.Timedelta(days=days), date + pd.Timedelta(days=days))
        output[rid] = frame.loc[keep].copy()
    return output


def lagged_samples(samples: dict[str, pd.DataFrame]) -> dict[str, pd.DataFrame]:
    output = {}
    for rid, frame in samples.items():
        lag = frame[["start_date", "end_date", "explanatory_excess_return"]].rename(columns={"start_date": "lag_start", "end_date": "start_date", "explanatory_excess_return": "lagged_explanatory_excess_return"})
        current = frame.drop(columns=["explanatory_excess_return"])
        merged = current.merge(lag[["start_date", "lagged_explanatory_excess_return"]], on="start_date", how="inner", validate="many_to_one")
        merged["explanatory_excess_return"] = merged.lagged_explanatory_excess_return
        output[rid] = merged
    return output


def rolling_plot(samples: dict[str, pd.DataFrame], cfg: dict, output: Path) -> pd.DataFrame:
    window, step, minimum = (cfg["rolling"][k] for k in ["window_observations", "step_observations", "minimum_observations"])
    rows = []
    fig, axes = plt.subplots(len(samples), 1, figsize=(10, 9), sharex=True)
    for ax, (rid, frame) in zip(np.atleast_1d(axes), samples.items()):
        for end in range(minimum, len(frame) + 1, step):
            sub = frame.iloc[max(0, end - window):end]
            result = sm.OLS(sub.dependent_excess_return, sm.add_constant(sub[["explanatory_excess_return"]], has_constant="add")).fit()
            beta = result.params["explanatory_excess_return"]
            se = result.bse["explanatory_excess_return"]
            rows.append({"relationship": rid, "end_date": sub.end_date.iloc[-1], "start_date": sub.start_date.iloc[0], "n": len(sub), "beta": beta, "ci_low": beta - 1.96 * se, "ci_high": beta + 1.96 * se})
        plot = pd.DataFrame([r for r in rows if r["relationship"] == rid])
        ax.plot(plot.end_date, plot.beta, lw=1.5)
        ax.fill_between(plot.end_date, plot.ci_low, plot.ci_high, alpha=.2)
        ax.axhline(0, color="black", lw=.7)
        ax.set_title(rid.replace("_", " "))
        ax.set_ylabel("rolling beta")
    axes[-1].set_xlabel("window end")
    fig.suptitle("Rolling 252-observation Design A coefficient (95% conventional CI)")
    fig.tight_layout()
    fig.savefig(output / "rolling_coefficients.png", dpi=160)
    plt.close(fig)
    return pd.DataFrame(rows)


def markdown_tables(coefficients: pd.DataFrame, cfg: dict) -> str:
    primary = coefficients[(coefficients.hac_lag == cfg["uncertainty"]["primary_hac_lag"]) & (coefficients.term.isin(["const", "explanatory_excess_return"]))]
    lines = ["# Coefficient tables", "", "Primary HAC lag 5. Returns are decimal USD price returns in excess of the common USD RF.", ""]
    for rid in primary.relationship.unique():
        lines += [f"## {rid}", "", "| Sample | Design | Term | Coefficient | 95% CI | p-value | N | Adj. R2 |", "|---|---|---|---:|---:|---:|---:|---:|"]
        for _, r in primary[primary.relationship == rid].iterrows():
            lines.append(f"| {r['sample']} | {r['design']} | {r['term']} | {r['coefficient']:.5f} | [{r['ci_low']:.5f}, {r['ci_high']:.5f}] | {r['p_value']:.4g} | {int(r['n'])} | {r['adjusted_r2']:.4f} |")
        lines.append("")
    return "\n".join(lines)


def write_report(output: Path, cfg: dict, audit: dict, model_rows: list[dict], diagnostics: list[dict], coefficients: pd.DataFrame) -> None:
    primary = coefficients[(coefficients["sample"] == "primary") & (coefficients.hac_lag == cfg["uncertainty"]["primary_hac_lag"]) & (coefficients.term == "explanatory_excess_return")]
    lines = [
        "# Prosus/Tencent/Naspers descriptive return regressions", "",
        "## Scope and status", "",
        "Nine frozen OLS specifications were completed as descriptive associations. They are not NAV-discount models, forecasts, causal estimates, or trading tests. The primary dependent and explanatory variables are exact-interval USD **price returns**, less the common USD risk-free rate; they are provisional as total-return evidence because packaged WRDS field definitions do not certify AJEXDI/TRFD mechanics and Tencent's in-specie distributions create vendor adjustment regimes.", "",
        "## Primary results", "", "| Relationship | Design | Stock-return beta | 95% HAC(5) CI | N | Adj. R2 |", "|---|---|---:|---:|---:|---:|",
    ]
    for _, r in primary.iterrows():
        lines.append(f"| {r.relationship} | {r.design} | {r.coefficient:.4f} | [{r.ci_low:.4f}, {r.ci_high:.4f}] | {int(r.n)} | {r.adjusted_r2:.4f} |")
    lines += [
        "", "Design A includes the explanatory stock return; B adds USD Euro Stoxx 50 and Hang Seng price returns; C adds both frozen regional FF5 blocks (Europe and Asia-Pacific ex Japan: Mkt-RF, SMB, HML, RMW, CMA). Both factor blocks are USD decimal series. Index constituent overlap, especially Tencent/Hang Seng, can mechanically raise fit and is not independent causal evidence.", "",
        "### Nested explanatory contribution", "", "| Relationship | Added block | Partial R2 | Adjusted R2 change |", "|---|---|---:|---:|",
    ]
    for row in model_rows:
        if row["design"] in {"B", "C"}:
            block = "market indices (B vs A)" if row["design"] == "B" else "regional FF5 blocks (C vs B)"
            lines.append(f"| {row['relationship']} | {block} | {row['partial_r2_vs_previous']:.4f} | {row['adjusted_r2_change_vs_previous']:.4f} |")
    lines += [
        "", "The market-index block adds most for the Tencent relationships; the FF5 increment is smaller, especially for Naspers on Prosus. These are in-sample descriptive increments on identical relationship-specific masks.", "",
        "## Ingestion integrity", "",
        f"Archive SHA-256, exact {audit['ingestion_integrity']['zip_member_count']} ZIP-member count, CRCs, safe paths, and all {audit['ingestion_integrity']['manifest_entries']} manifest-listed payload hashes passed. The licensed bundle remains under Git-ignored `data/`.", "",
        "## Alignment and exclusions", "",
    ]
    for rid, a in audit["attrition"].items():
        lines.append(f"- {rid}: {a['common_model_sample']} common observations, {a['first_end_date']} to {a['last_end_date']}; {a['exact_pair_intervals']} exact stock-pair intervals before factor/market/date restrictions.")
    lines += [
        "", "Returns were joined only when start and end dates matched exactly across both stocks, both market indices, ECB FX endpoints, and both factor blocks. Exchange holidays were not forward-filled. WRDS flag-5 carry-forwards, returns touching them, adjustment-factor changes, and split markers were excluded with reasons retained in `exclusions_alignment.csv`. Large returns were otherwise retained.", "",
        "Contemporaneous local-date matching is imperfect because Hong Kong closes before Europe/Johannesburg and the ECB fixing is not an HK close quote. The bounded one-interval-lag results are reported separately and must not be interpreted predictively.", "",
        "## Corporate actions and basis qualifications", "",
        "- Tencent's JD.com (2022-01-20) and Meituan (2023-01-05) ex-dates can transfer value outside the cash close and differ across vendor adjustment regimes; the action-window sensitivity removes declared windows.",
        "- The 2023 cross-holding reorganisation removed the Prosus/Naspers cross-holding while preserving the approximate 57%/43% free-float economic interests through capitalisation/consolidation actions. Adjustment changes are excluded; a declared window sensitivity is provided.",
        "- Naspers completed a five-for-one split in October 2025. The action/adjustment boundary is excluded and tested with a wider window.",
        "- The Prosus 2020-10-19 >10bp Yahoo/WRDS diagnostic discrepancy is flagged in the same action-window sensitivity. AJEXDI division is not used as a return formula.",
        "- Yahoo's 179 Naspers OHLC violations do not enter these close-only WRDS regressions. November 2 company-feed closes are excluded because they are not certified adjusted observations and factor coverage ends September 30, 2026.", "",
        "## Diagnostics and limitations", "",
        "HAC(5) is primary and HAC(20) is included in `coefficients.csv`. Primary residuals reject normality and Ljung-Box no-autocorrelation tests at conventional levels; several Tencent Design B/C specifications also reject homoskedasticity. HAC uncertainty is therefore essential, but it does not repair return-basis ambiguity. Design C standardized condition numbers are below 7.5 and maximum VIFs below 7.2. Full values are in `model_summary.json`.", "",
        "The ±5-calendar-day corporate-action sensitivity leaves the core betas materially similar. In the one-interval-lag Design C sensitivity, stock-return coefficients are small and their 95% intervals include zero for all three relationships; this is a timing diagnostic, not a predictive test. Rolling coefficients use a declared 252-observation window stepped by 21 observations.", "",
        "Historical point-in-time NAV, borrow availability/fees, implementation costs, and complete publication-time event histories remain missing. They are not required for these descriptive return regressions and were not imputed. No quarterly NAV was forward-filled; CSHOC and consolidated cash/debt were not used.", "",
        "## Reproduction", "",
        "Run `sbatch slurm/prosus_tencent_returns.sbatch`. The job records config and input hashes, package versions, and Slurm metadata in this run directory.", "",
    ]
    (output / "REPORT.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    parser.add_argument("--run-id")
    parser.add_argument("--validate-only", action="store_true")
    args = parser.parse_args()
    config_path = args.config.resolve()
    cfg = read_config(config_path)
    bundle = (ROOT / cfg["bundle_root"]).resolve()
    integrity = verify_bundle_integrity(bundle)
    samples, exclusions, audit = build_relationship_samples(bundle, cfg)
    audit["ingestion_integrity"] = integrity
    for rid, frame in samples.items():
        if len(frame) < 500:
            raise ValueError(f"unexpectedly small common sample for {rid}: {len(frame)}")
        diag = matrix_diagnostics(frame, cfg["designs"]["C"])
        audit.setdefault("pre_fit_collinearity", {})[rid] = diag
        if not math.isfinite(diag["condition_number_standardized"]) or diag["condition_number_standardized"] > 100:
            raise ValueError(f"invalid/high collinearity for frozen design C, {rid}: {diag}")
    if args.validate_only:
        print(json.dumps({"status": "validated", "audit": audit}, indent=2, default=str))
        return 0
    run_id = args.run_id or datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    output = ROOT / cfg["output_root"] / run_id
    output.mkdir(parents=True, exist_ok=False)
    (output / "config.json").write_text(json.dumps(cfg, indent=2) + "\n", encoding="utf-8")
    exclusions.to_csv(output / "exclusions_alignment.csv", index=False)
    pd.concat(samples.values(), ignore_index=True).to_csv(output / "common_samples.csv", index=False)
    primary_coeff, primary_models, primary_diag = fit_models(samples, cfg, "primary")
    action_coeff, action_models, action_diag = fit_models(action_window_samples(samples, cfg), cfg, "action_window_excluded")
    lag_coeff, lag_models, lag_diag = fit_models(lagged_samples(samples), cfg, "explanatory_lag_1_interval")
    coefficients = pd.concat([primary_coeff, action_coeff, lag_coeff], ignore_index=True)
    coefficients.to_csv(output / "coefficients.csv", index=False)
    rolling_plot(samples, cfg, output).to_csv(output / "rolling_coefficients.csv", index=False)
    model_summary = {"models": primary_models + action_models + lag_models, "diagnostics": primary_diag + action_diag + lag_diag, "audit": audit}
    (output / "model_summary.json").write_text(json.dumps(model_summary, indent=2, default=str) + "\n", encoding="utf-8")
    (output / "ingestion_integrity.json").write_text(json.dumps(integrity, indent=2) + "\n", encoding="utf-8")
    (output / "COEFFICIENT_TABLES.md").write_text(markdown_tables(coefficients, cfg) + "\n", encoding="utf-8")
    input_paths = [config_path, ROOT / "data/prosus_tencent_validated_2026-11-02.zip", ROOT / "data/prosus_tencent_validated_2026-11-02.zip.sha256", bundle / "logs/package_manifest.json", bundle / "data/processed/wrds_security_daily_research.csv", bundle / "data/raw/ecb_fx_daily_long.csv", bundle / "data/raw/euro_stoxx_50.csv", bundle / "data/raw/hang_seng.csv"] + [bundle / "data/processed" / name for name in cfg["factor_blocks"].values()]
    provenance = {
        "created_utc": datetime.now(timezone.utc).isoformat(), "run_id": run_id, "command": sys.argv,
        "python": sys.version, "platform": platform.platform(), "slurm_job_id": os.getenv("SLURM_JOB_ID"),
        "versions": {"numpy": np.__version__, "pandas": pd.__version__, "statsmodels": sm.__version__, "matplotlib": matplotlib.__version__},
        "inputs": [{"path": str(p.relative_to(ROOT)), "bytes": p.stat().st_size, "sha256": sha256(p)} for p in input_paths],
        "script": {"path": str(Path(__file__).resolve().relative_to(ROOT)), "sha256": sha256(Path(__file__).resolve())},
        "return_basis": "WRDS PRCSTD=10 close-to-close USD price returns with exact ECB endpoints; not certified total returns",
    }
    (output / "provenance.json").write_text(json.dumps(provenance, indent=2) + "\n", encoding="utf-8")
    write_report(output, cfg, audit, primary_models, primary_diag, coefficients)
    print(json.dumps({"status": "complete", "output": str(output), "common_samples": audit["attrition"]}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
