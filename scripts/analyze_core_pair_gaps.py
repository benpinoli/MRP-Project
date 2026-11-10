#!/usr/bin/env python3
"""Run Samsung-style B01-B04 regressions for a validated two-security panel."""
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
from samsung_research.regressions import align_preceding_us_sessions, fit_ols  # noqa: E402


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def markdown_table(frame: pd.DataFrame) -> str:
    """Render Markdown without the optional tabulate dependency."""
    clean = frame.astype(object).where(frame.notna(), "").astype(str)
    header = "| " + " | ".join(clean.columns) + " |"
    rule = "| " + " | ".join(["---"] * len(clean.columns)) + " |"
    rows = ["| " + " | ".join(value.replace("|", "\\|") for value in row) + " |"
            for row in clean.to_numpy()]
    return "\n".join([header, rule, *rows])


def bh_adjust(values: pd.Series) -> pd.Series:
    output = pd.Series(np.nan, index=values.index, dtype=float)
    valid = values.dropna().sort_values()
    if valid.empty:
        return output
    n = len(valid)
    adjusted = (valid.to_numpy() * n / np.arange(1, n + 1))[::-1]
    adjusted = np.minimum.accumulate(adjusted)[::-1]
    output.loc[valid.index] = np.minimum(adjusted, 1.0)
    return output


def exact_fx(path: Path) -> pd.DataFrame:
    fx = pd.read_csv(path, parse_dates=["date"])
    wide = fx.pivot(index="date", columns="currency", values="foreign_units_per_EUR").sort_index()
    wide["EUR"] = 1.0
    if not (wide > 0).all().all():
        raise ValueError("FX panel contains missing or nonpositive observed rates")
    return wide


def security_panel(raw: pd.DataFrame, spec: dict, fx: pd.DataFrame, prefix: str, required_prcstd: int) -> pd.DataFrame:
    frame = raw[(raw.gvkey.astype(str) == spec["gvkey"]) & (raw.iid.astype(str) == spec["iid"])].copy()
    frame = frame.sort_values("datadate").reset_index(drop=True)
    observed = {
        "name": sorted(frame.conm.dropna().unique()),
        "currency": sorted(frame.curcdd.dropna().unique()),
    }
    if observed != {"name": [spec["name"]], "currency": [spec["currency"]]}:
        raise ValueError(f"identity audit failed for {prefix}: {observed}")
    frame["date"] = pd.to_datetime(frame.datadate)
    local = pd.to_numeric(frame.prccd, errors="coerce") / pd.to_numeric(frame.qunit, errors="coerce")
    rates = fx[spec["currency"]].reindex(frame.date).to_numpy()
    usd = fx["USD"].reindex(frame.date).to_numpy()
    frame[f"{prefix}_price"] = local.to_numpy() / rates * usd
    frame[f"{prefix}_volume"] = pd.to_numeric(frame.cshtrd, errors="coerce")
    reported = pd.to_numeric(frame.prcstd, errors="coerce").eq(required_prcstd)
    unchanged = pd.to_numeric(frame.ajexdi, errors="coerce").eq(pd.to_numeric(frame.ajexdi, errors="coerce").shift())
    no_split = frame[["split", "splitf"]].fillna(0).eq(0).all(axis=1)
    exact = frame.date.isin(fx.index)
    positive = frame[f"{prefix}_price"].gt(0)
    frame[f"{prefix}_usable"] = reported & unchanged & no_split & exact & positive
    return frame[["date", f"{prefix}_price", f"{prefix}_volume", f"{prefix}_usable"]]


def build_panel(cfg: dict, paths: dict[str, Path]) -> tuple[pd.DataFrame, pd.DataFrame, dict]:
    raw = pd.read_csv(paths["security_daily"], dtype={"gvkey": str, "iid": str})
    fx = exact_fx(paths["fx"])
    required = cfg["sample"]["required_prcstd"]
    num = security_panel(raw, cfg["pair"]["numerator"], fx, "numerator", required)
    den = security_panel(raw, cfg["pair"]["denominator"], fx, "denominator", required)
    panel = num.merge(den, on="date", how="inner", validate="one_to_one").sort_values("date").reset_index(drop=True)
    panel = panel[panel.date.between(cfg["sample"]["start"], cfg["sample"]["end"])].copy()
    usable = panel.numerator_usable & panel.denominator_usable
    ratio = panel.numerator_price / panel.denominator_price
    anchor = float(ratio[usable].iloc[0])
    panel["discount_pct"] = np.where(usable, 100 * (1 - ratio / anchor), np.nan)
    panel["dg"] = np.log(panel.denominator_price * anchor / panel.numerator_price).where(usable)
    panel["dd_pp"] = panel.discount_pct.diff()
    panel["dg"] = panel.dg.diff()
    panel["lag_discount"] = panel.discount_pct.shift()
    activity = np.log((panel.numerator_volume / panel.denominator_volume).where(
        (panel.numerator_volume > 0) & (panel.denominator_volume > 0)
    ))
    panel["lag_activity"] = activity.shift()
    # Diff/lag operations must not bridge an unusable endpoint.
    adjacent = usable & usable.shift(fill_value=False)
    panel.loc[~adjacent, ["dd_pp", "dg", "lag_discount", "lag_activity"]] = np.nan

    sessions = pd.DataFrame({"date": panel.date.dt.strftime("%Y-%m-%d")})
    factors = pd.read_csv(paths["factors"])
    aligned, mapping = align_preceding_us_sessions(
        sessions, factors, cfg["factor_names"], 0.01
    )
    panel = pd.concat([panel.reset_index(drop=True), aligned], axis=1)
    panel["date"] = panel.date.dt.strftime("%Y-%m-%d")
    panel["grid_index"] = np.arange(len(panel))
    audit = {
        "common_date_rows": int(len(panel)),
        "usable_level_rows": int(usable.sum()),
        "first_date": panel.date.min(),
        "last_date": panel.date.max(),
        "normalization_anchor_first_usable_usd_price_ratio": anchor,
        "outcome_interpretation": "100 * (1 - current USD price ratio / first usable USD price ratio); not NAV discount",
    }
    return panel, mapping, audit


def fit_all(panel: pd.DataFrame, cfg: dict) -> tuple[pd.DataFrame, pd.DataFrame]:
    factors = ["F_" + name for name in cfg["factor_names"]]
    coef_rows: list[dict] = []
    model_rows: list[dict] = []
    event_days = cfg["sensitivity_event_window_calendar_days"]
    event_dates = [pd.Timestamp(event["date"]) for event in cfg["sensitivity_events"]]
    dates = pd.to_datetime(panel.date)
    sensitivity_keep = pd.Series(True, index=panel.index)
    for event_date in event_dates:
        sensitivity_keep &= ~dates.between(event_date - pd.Timedelta(days=event_days), event_date + pd.Timedelta(days=event_days))

    for variant, variant_keep in (("main", pd.Series(True, index=panel.index)), ("sensitivity", sensitivity_keep)):
        for window in cfg["windows"]:
            window_keep = dates.between(window["start"], window["end"])
            for model in cfg["models"]:
                columns = factors + model["columns"]
                needed = [model["outcome"], *columns]
                sample = panel.loc[variant_keep & window_keep].dropna(subset=needed)
                for hac in cfg["hac_lags"]:
                    base = {"pair": cfg["pair"]["id"], "model": model["id"], "variant": variant, "window": window["id"], "hac_lag": hac}
                    try:
                        x = np.column_stack([np.ones(len(sample)), sample[columns].to_numpy(float)])
                        coefficient, standard_error, p_value, _, diagnostics = fit_ols(
                            sample[model["outcome"]],
                            x,
                            sample.grid_index,
                            hac,
                            minimum=cfg["minimum_observations"],
                        )
                    except ValueError as exc:
                        model_rows.append({**base, "status": "blocked", "detail": str(exc), "n": int(len(sample))})
                        continue
                    terms = ["intercept", *columns]
                    for i, term in enumerate(terms):
                        coef_rows.append({**base, "term": term, "coefficient": coefficient[i], "standard_error": standard_error[i], "p_value": p_value[i], "n": diagnostics["n"], "adjusted_r2": diagnostics["adjusted_r_squared"]})
                    model_rows.append({**base, "status": "estimated", "detail": "", "n": diagnostics["n"], "adjusted_r2": diagnostics["adjusted_r_squared"], "condition_number": diagnostics["standardized_condition"]})
    coefficients = pd.DataFrame(coef_rows)
    if not coefficients.empty:
        test = coefficients.term.ne("intercept")
        coefficients["q_value_bh"] = np.nan
        coefficients.loc[test, "q_value_bh"] = bh_adjust(coefficients.loc[test, "p_value"])
    return coefficients, pd.DataFrame(model_rows)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="configs/core_pair_gap_regressions.v1.json")
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    config_path = ROOT / args.config
    cfg = json.loads(config_path.read_text(encoding="utf-8"))
    paths = {name: ROOT / value for name, value in cfg["inputs"].items()}
    missing = [str(path) for path in paths.values() if not path.is_file()]
    if missing:
        raise FileNotFoundError(f"missing inputs: {missing}")
    metadata = json.loads(paths["factor_metadata"].read_text(encoding="utf-8"))
    if metadata["units"] != "percent" or metadata["point_in_time_forecasting_valid"] is not False:
        raise ValueError("factor metadata no longer matches frozen retrospective design")
    output = ROOT / args.output
    output.mkdir(parents=True, exist_ok=False)
    panel, mapping, audit = build_panel(cfg, paths)
    coefficients, models = fit_all(panel, cfg)
    panel.to_csv(output / "panel.csv", index=False)
    mapping.to_csv(output / "factor_alignment.csv", index=False)
    coefficients.to_csv(output / "coefficients.csv", index=False)
    models.to_csv(output / "model_status.csv", index=False)
    manifest = {
        "config": str(config_path.relative_to(ROOT)),
        "config_sha256": digest(config_path),
        "inputs": {str(path.relative_to(ROOT)): digest(path) for path in paths.values()},
        "audit": audit,
        "estimated": int((models.status == "estimated").sum()),
        "blocked": int((models.status == "blocked").sum()),
    }
    (output / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    primary = models[(models.hac_lag == 20) & (models.variant == "main")]
    report = [
        "# Prosus/Tencent Samsung-style gap regressions",
        "",
        "These are retrospective normalized USD price-ratio associations, not a Prosus NAV discount, fair-value model, forecast, causal estimate, or trading test.",
        "",
        f"Estimated task specifications: {manifest['estimated']}; blocked: {manifest['blocked']}.",
        "",
        "## Primary HAC(20) model status",
        "",
        markdown_table(primary),
        "",
        "The gap normalization uses the first usable contemporaneous USD price ratio only to put the series in percentage-point units. It has no fair-value interpretation.",
    ]
    (output / "REPORT.md").write_text("\n".join(report) + "\n", encoding="utf-8")
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
