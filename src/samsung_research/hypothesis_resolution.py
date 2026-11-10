"""Mechanism-discrimination analyses for questions currently supported by local data."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import norm, spearmanr

from samsung_research.regressions import fit_ols


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def require(condition: bool, detail: str) -> None:
    if not condition:
        raise ValueError(detail)


def markdown(frame: pd.DataFrame) -> str:
    clean = frame.astype(object).where(frame.notna(), "").astype(str)
    head = "| " + " | ".join(clean.columns) + " |"
    rule = "| " + " | ".join(["---"] * len(clean.columns)) + " |"
    rows = ["| " + " | ".join(v.replace("|", "\\|") for v in row) + " |" for row in clean.to_numpy()]
    return "\n".join([head, rule, *rows])


def hc1_ols(y: np.ndarray, x: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray, float]:
    require(len(y) > x.shape[1], "insufficient OLS observations")
    require(np.linalg.matrix_rank(x) == x.shape[1], "rank-deficient OLS design")
    inv = np.linalg.inv(x.T @ x)
    b = inv @ x.T @ y
    e = y - x @ b
    scores = x * e[:, None]
    cov = inv @ (scores.T @ scores) @ inv * len(y) / (len(y) - x.shape[1])
    se = np.sqrt(np.maximum(np.diag(cov), 0))
    p = 2 * norm.sf(np.abs(b / se))
    r2 = 1 - (e @ e) / ((y - y.mean()) @ (y - y.mean()))
    return b, se, p, r2


def residualize(value: np.ndarray, nuisance: np.ndarray | None) -> np.ndarray:
    if nuisance is None or nuisance.size == 0:
        z = np.ones((len(value), 1))
    else:
        z = np.column_stack([np.ones(len(value)), nuisance])
    return value - z @ np.linalg.lstsq(z, value, rcond=None)[0]


def partial_permutation_p(y: np.ndarray, target: np.ndarray, nuisance: np.ndarray | None,
                          permutations: int, rng: np.random.Generator) -> float:
    yr = residualize(y, nuisance)
    xr = residualize(target, nuisance)
    observed = abs(float(np.corrcoef(yr, xr)[0, 1]))
    exceed = 0
    for _ in range(permutations):
        exceed += abs(float(np.corrcoef(rng.permutation(yr), xr)[0, 1])) >= observed
    return (exceed + 1) / (permutations + 1)


def annual_supply(path: Path, spec: dict) -> tuple[pd.DataFrame, pd.DataFrame, dict]:
    data = pd.read_csv(path)
    level = data[data.joint_eligible.astype(str).str.lower().eq("true")].copy()
    require(len(level) == 17, "annual joint sample changed")
    supply = "preferred_to_common_nontreasury"
    activity = "preferred_to_common_activity"
    ycol = "mean_monthly_q"
    level["time"] = level.year - level.year.mean()
    change = level[level.year.between(2010, 2025)].copy()
    require(change.year.tolist() == list(range(2010, 2026)), "annual change sample is not consecutive")
    change["dq"] = change[ycol].diff()
    change["dsupply"] = change[supply].diff()
    change["dactivity"] = change[activity].diff()
    change = change.dropna(subset=["dq", "dsupply", "dactivity"]).copy()
    rng = np.random.default_rng(spec["seed"])
    rows = []

    def fit(sample: pd.DataFrame, model: str, outcome: str, predictors: list[str], permutation_targets: list[str]) -> None:
        y = sample[outcome].to_numpy(float)
        x = np.column_stack([np.ones(len(sample)), sample[predictors].to_numpy(float)])
        b, se, p, r2 = hc1_ols(y, x)
        for i, term in enumerate(["intercept", *predictors]):
            perm = np.nan
            if term in permutation_targets:
                nuisance_names = [v for v in predictors if v != term]
                nuisance = sample[nuisance_names].to_numpy(float) if nuisance_names else None
                perm = partial_permutation_p(y, sample[term].to_numpy(float), nuisance,
                                             spec["permutations"], rng)
            rows.append({"model": model, "term": term, "coefficient": b[i], "hc1_se": se[i],
                         "normal_p": p[i], "partial_permutation_p": perm, "n": len(sample), "r2": r2})

    fit(level, "A1_levels_supply", ycol, [supply], [supply])
    fit(level, "A2_levels_activity", ycol, [activity], [activity])
    fit(level, "A3_levels_joint_time", ycol, [supply, activity, "time"], [supply, activity])
    fit(change, "A4_changes_supply", "dq", ["dsupply"], ["dsupply"])
    fit(change, "A5_changes_activity", "dq", ["dactivity"], ["dactivity"])
    fit(change, "A6_changes_joint", "dq", ["dsupply", "dactivity"], ["dsupply", "dactivity"])
    results = pd.DataFrame(rows)

    diagnostics = []
    for sample_name, frame, cols in (
        ("levels", level, [ycol, supply, activity]),
        ("changes", change, ["dq", "dsupply", "dactivity"]),
    ):
        for variable in cols[1:]:
            rho, p = spearmanr(frame[cols[0]], frame[variable])
            diagnostics.append({"sample": sample_name, "outcome": cols[0], "variable": variable,
                                "spearman_rho": rho, "spearman_p": p, "n": len(frame)})
    stable = level[level.year.between(spec["stable_supply_start"], spec["stable_supply_end"])]
    summary = {
        "joint_level_years": level.year.astype(int).tolist(),
        "consecutive_change_years": change.year.astype(int).tolist(),
        "stable_supply_period": f"{spec['stable_supply_start']}-{spec['stable_supply_end']}",
        "stable_supply_ratio_min": float(stable[supply].min()),
        "stable_supply_ratio_max": float(stable[supply].max()),
        "stable_discount_min": float(stable[ycol].min()),
        "stable_discount_max": float(stable[ycol].max()),
        "stable_discount_range_pp": float(stable[ycol].max() - stable[ycol].min()),
    }
    return results, pd.DataFrame(diagnostics), summary


def samsung_adjustment(raw_path: Path, grid_path: Path, spec: dict) -> tuple[pd.DataFrame, pd.DataFrame]:
    raw = pd.read_csv(raw_path, dtype={"gvkey": str, "iid": str})
    raw = raw[raw.gvkey.eq("104604") & raw.iid.isin(["01W", "02W"])].copy()
    raw["date"] = pd.to_datetime(raw.datadate)
    raw["adjusted_close"] = pd.to_numeric(raw.prccd) / pd.to_numeric(raw.ajexdi) / pd.to_numeric(raw.qunit)
    require(not raw.duplicated(["iid", "date"]).any(), "duplicate Samsung security date")
    wide = raw.pivot(index="date", columns="iid", values="adjusted_close").rename(columns={"01W": "preferred", "02W": "common"}).reset_index()
    grid = pd.read_csv(grid_path)
    grid["date"] = pd.to_datetime(grid.date)
    grid["flagged"] = grid.flagged.astype(str).str.lower().eq("true")
    grid["observed_session"] = grid.observed_session.astype(str).str.lower().eq("true")
    panel = grid[grid.observed_session].merge(wide, on="date", how="left", validate="one_to_one").sort_values("date").reset_index(drop=True)
    price_valid = panel[["common", "preferred"]].notna().all(axis=1) & panel[["common", "preferred"]].gt(0).all(axis=1)
    panel["signal_dd_pp"] = pd.to_numeric(panel.discount_pct).diff()
    panel.loc[panel.flagged | panel.flagged.shift(fill_value=False) | ~price_valid | ~price_valid.shift(fill_value=False), "signal_dd_pp"] = np.nan
    rows, samples = [], []
    dates = panel.date
    for horizon in spec["horizons_sessions"]:
        invalid_endpoint = panel.flagged | ~price_valid
        interval_bad = invalid_endpoint.rolling(horizon + 1).max().shift(-horizon).fillna(1).astype(bool)
        panel[f"common_h{horizon}"] = np.log(panel.common.shift(-horizon) / panel.common).where(~interval_bad)
        panel[f"preferred_h{horizon}"] = np.log(panel.preferred.shift(-horizon) / panel.preferred).where(~interval_bad)
        panel[f"relative_h{horizon}"] = panel[f"preferred_h{horizon}"] - panel[f"common_h{horizon}"]
        for window in spec["windows"]:
            window_mask = dates.between(window["start"], window["end"])
            for outcome in ("common", "preferred", "relative"):
                col = f"{outcome}_h{horizon}"
                sample = panel.loc[window_mask].dropna(subset=["signal_dd_pp", col])
                base = {"hypothesis": "M04_B03_leg_adjustment", "window": window["id"], "horizon": horizon,
                        "outcome": outcome, "n": len(sample),
                        "sample_start": sample.date.min().strftime("%Y-%m-%d") if len(sample) else "",
                        "sample_end": sample.date.max().strftime("%Y-%m-%d") if len(sample) else ""}
                try:
                    x = np.column_stack([np.ones(len(sample)), sample.signal_dd_pp.to_numpy(float)])
                    b, se, p, _, diag = fit_ols(sample[col], x, sample.index.to_numpy(), max(5, horizon), minimum=spec["minimum_observations"])
                    rows.append({**base, "status": "estimated", "coefficient_on_widening": b[1], "hac_se": se[1],
                                 "p_value": p[1], "adjusted_r2": diag["adjusted_r_squared"]})
                except ValueError as exc:
                    rows.append({**base, "status": "blocked", "detail": str(exc)})
                samples.append(base)
    return pd.DataFrame(rows), panel


def tsmc_discovery(path: Path, spec: dict) -> tuple[pd.DataFrame, pd.DataFrame, dict]:
    panel = pd.read_csv(path, low_memory=False)
    panel = panel[panel.pair.eq("tsmc_local_adr")].copy()
    panel["date"] = pd.to_datetime(panel.date)
    panel = panel.sort_values("date").reset_index(drop=True)
    local = panel.dropna(subset=["local_adjusted_close"])[["date", "local_adjusted_close"]].copy()
    adr = panel.dropna(subset=["adr_adjusted_close"])[["date", "adr_adjusted_close", "adr_bid", "adr_ask"]].copy()
    fx = panel.dropna(subset=["DEXTAUS"])[["date", "DEXTAUS"]].copy()
    local["next_local_date"] = local.date.shift(-1)
    local["next_local_return"] = np.log(local.local_adjusted_close.shift(-1) / local.local_adjusted_close)
    adr["previous_adr_close"] = adr.adr_adjusted_close.shift()
    adr["adr_return_from_previous"] = np.log(adr.adr_adjusted_close / adr.previous_adr_close)
    adr["relative_spread"] = (adr.adr_ask - adr.adr_bid) / ((adr.adr_ask + adr.adr_bid) / 2)

    # Taiwan-close state: only prior ADR and prior FX are allowed; outcome is the later same-date ADR move.
    prior_adr = adr[["date", "adr_adjusted_close"]].rename(columns={"date": "prior_adr_date", "adr_adjusted_close": "prior_adr_close"})
    prior_fx = fx.rename(columns={"date": "prior_fx_date", "DEXTAUS": "prior_fx"})
    taiwan = pd.merge_asof(local.sort_values("date"), prior_adr, left_on="date", right_on="prior_adr_date", direction="backward", allow_exact_matches=False)
    taiwan = pd.merge_asof(taiwan.sort_values("date"), prior_fx, left_on="date", right_on="prior_fx_date", direction="backward", allow_exact_matches=False)
    taiwan = taiwan.merge(adr[["date", "adr_return_from_previous", "relative_spread"]], on="date", how="left", validate="one_to_one")
    taiwan["gap_at_taiwan_close_log"] = np.log(taiwan.prior_adr_close / (5 * taiwan.local_adjusted_close / taiwan.prior_fx))

    # US-close state: same-date local and noon-NY FX are known by the US close; outcome is next Taiwan-session local move.
    us = adr.merge(local[["date", "local_adjusted_close", "next_local_date", "next_local_return"]], on="date", how="inner", validate="one_to_one")
    us = us.merge(fx, on="date", how="left", validate="one_to_one")
    us["gap_at_us_close_log"] = np.log(us.adr_adjusted_close / (5 * us.local_adjusted_close / us.DEXTAUS))
    spread_cut = float(adr.relative_spread.dropna().quantile(spec["spread_exclusion_quantile"]))
    rows = []

    def estimate(frame: pd.DataFrame, clock: str, predictor: str, outcome: str, window: dict, variant: str) -> None:
        sample = frame[frame.date.between(window["start"], window["end"])].dropna(subset=[predictor, outcome]).copy()
        if variant == "spread_sensitivity":
            sample = sample[sample.relative_spread.le(spread_cut)]
        base = {"hypothesis": "X02_M04_price_discovery", "clock": clock, "variant": variant, "window": window["id"],
                "predictor": predictor, "outcome": outcome, "n": len(sample),
                "sample_start": sample.date.min().strftime("%Y-%m-%d") if len(sample) else "",
                "sample_end": sample.date.max().strftime("%Y-%m-%d") if len(sample) else ""}
        try:
            x = np.column_stack([np.ones(len(sample)), sample[predictor].to_numpy(float)])
            b, se, p, _, diag = fit_ols(sample[outcome], x, sample.index.to_numpy(), spec["hac_lag"], minimum=spec["minimum_observations"])
            rows.append({**base, "status": "estimated", "coefficient": b[1], "hac_se": se[1], "p_value": p[1],
                         "adjusted_r2": diag["adjusted_r_squared"]})
        except ValueError as exc:
            rows.append({**base, "status": "blocked", "detail": str(exc)})

    for window in spec["windows"]:
        estimate(taiwan, "taiwan_close_to_same_day_us_close", "gap_at_taiwan_close_log", "adr_return_from_previous", window, "main")
        estimate(us, "us_close_to_next_taiwan_close", "gap_at_us_close_log", "next_local_return", window, "main")
        estimate(taiwan, "taiwan_close_to_same_day_us_close", "gap_at_taiwan_close_log", "adr_return_from_previous", window, "spread_sensitivity")
        estimate(us, "us_close_to_next_taiwan_close", "gap_at_us_close_log", "next_local_return", window, "spread_sensitivity")
    audit = {"adr_relative_spread_90pct_cutoff": spread_cut,
             "taiwan_clock_rule": "prior ADR close and latest FX fixing strictly before Taiwan calendar date; outcome later same-date ADR price return",
             "us_clock_rule": "same-date Taiwan close and noon-New-York FX at US close; outcome next Taiwan-session local price return"}
    return pd.DataFrame(rows), pd.concat([taiwan.assign(clock="taiwan"), us.assign(clock="us")], ignore_index=True, sort=False), audit


def event_summary(path: Path) -> tuple[pd.DataFrame, pd.DataFrame]:
    windows = pd.read_csv(path / "event_windows.csv")
    doses = pd.read_csv(path / "dose_arithmetic.csv")
    return windows, doses


def report(annual: pd.DataFrame, annual_diag: pd.DataFrame, annual_summary: dict,
           samsung: pd.DataFrame, tsmc: pd.DataFrame, tsmc_audit: dict,
           events: pd.DataFrame, doses: pd.DataFrame) -> str:
    a = annual[annual.term.ne("intercept")].copy()
    a = a[["model", "term", "coefficient", "hc1_se", "normal_p", "partial_permutation_p", "n", "r2"]]
    s = samsung[(samsung.window == "full") & samsung.status.eq("estimated")].copy()
    s = s[["horizon", "outcome", "coefficient_on_widening", "hac_se", "p_value", "n", "adjusted_r2"]]
    t = tsmc[(tsmc.window == "full") & tsmc.status.eq("estimated")].copy()
    t = t[["clock", "variant", "coefficient", "hac_se", "p_value", "n", "adjusted_r2"]]
    e = events[(events.base_rule == "next_proxy_session") & events.status.eq("ok")].copy()
    e = e[["event_id", "cluster", "kind", "publication_date", "h", "base_date", "target_date", "change_pp", "strict_interval"]]
    lines = [
        "# Hypothesis-resolution batch results", "", "Run date: November 9, 2026", "",
        "This batch uses already-qualified local inputs. It is retrospective and mechanism-discriminating, not causal, point-in-time forecasting, fair-value, or trading evidence.", "",
        "## Executive outcome", "",
        "Four ready questions were tested. The annual Samsung panel rejects a simple claim that relative non-treasury share supply alone explains recent discount movement: the count ratio was essentially flat in 2018–2023 while the annual discount spanned a wide range. The daily Samsung decomposition identifies which price leg followed widening episodes but remains an in-sample response description. Sparse issuer disclosures provide case studies, not independent event-regression evidence. The TSMC clock split tests whether adjustment occurs later in the US or at the next Taiwan close.", "",
        "## H1 — Samsung public-share supply versus trading capacity (S06/L01)", "",
        "**Hypothesis.** Persistent discount changes are associated with relative non-treasury supply and/or relative trading activity. Supply scarcity and impaired trading capacity are competing channels.", "",
        "**Regression.** Annual HC1 OLS in levels and first differences; joint models include both mechanisms, levels also include a linear time control. Partial permutation p-values use 20,000 fixed-seed permutations. With only 17 level years and 15 consecutive changes, inference is descriptive and small-sample.", "", markdown(a), "",
        "Rank diagnostics:", "", markdown(annual_diag), "",
        f"**Stable-supply falsification.** In {annual_summary['stable_supply_period']}, the preferred/common non-treasury ratio ranged only {annual_summary['stable_supply_ratio_min']:.6f}–{annual_summary['stable_supply_ratio_max']:.6f}, while the annual mean discount ranged {annual_summary['stable_discount_min']:.2f}–{annual_summary['stable_discount_max']:.2f} pp (range {annual_summary['stable_discount_range_pp']:.2f} pp).",
        "", "**Question answered.** Relative supply can describe long-run regimes but is not sufficient to explain material within-regime discount movement. Whether trading capacity or another omitted regime variable explains the remaining movement depends on the activity results above; raw volume is not a spread, signed flow, or public-float measure.", "",
        "## H2 — Which Samsung leg adjusts after a widening? (M04/B03)", "",
        "**Hypothesis.** If a widening is transient, later preferred returns should be positive relative to common returns. A negative common coefficient instead indicates common-price reversal.", "",
        "**Regression.** Adjusted-price forward log returns at 1/5/20 observed sessions on the current discount change. Flagged intervals are excluded; Newey–West lag is max(5,horizon). Coefficients are log-return response per one percentage-point widening.", "", markdown(s), "",
        "**Question answered.** The common, preferred, and relative-return rows show which leg contributes to subsequent adjustment. This is a full-sample decomposition, not an unexposed forecast test, and cannot identify investor type or execution costs.", "",
        "## H3 — Issuer repurchase, cancellation, and payout disclosures (S01/S02/S03/P01)", "",
        "**Hypothesis.** Preferred-relative support should narrow the discount after the information becomes observable; cancellation should not be double-counted as a second purchase.", "",
        "**Design.** Predeclared 1/5/20-session descriptive windows from the conservative next observed proxy session. Publication clocks are unavailable. Six disclosures collapse to three clusters; no iid event regression is claimed.", "", markdown(e), "",
        "Relative authorization/execution dose arithmetic:", "", markdown(doses), "",
        "**Question answered.** The table records what happened after each dated disclosure. It cannot separate program anticipation, management response to the existing discount, or overlapping stages of the same program.", "",
        "## H4 — TSMC cross-market price discovery (X02/X03/M04)", "",
        "**Hypothesis.** A parity gap measured at the Taiwan close predicts the later US ADR adjustment; a gap at the US close predicts the next Taiwan-local adjustment. The signs distinguish the market that moves toward parity.", "",
        "**Regression.** Timing-aware error-correction regressions with HAC(5). Taiwan-close states use only the prior ADR close and prior FX fixing. US-close states use the same-date Taiwan close and noon-New-York FX. A spread sensitivity excludes ADR relative spreads above the historical 90th percentile.", "", markdown(t), "",
        f"Spread cutoff: {tsmc_audit['adr_relative_spread_90pct_cutoff']:.6f}. {tsmc_audit['taiwan_clock_rule']}. {tsmc_audit['us_clock_rule']}.", "",
        "**Question answered.** The two clock-specific coefficients identify whether observed parity correction is concentrated in the later US session, the next Taiwan session, both, or neither. This does not establish executable arbitrage because local bid/ask, conversion fees, borrow, and creation/cancellation constraints remain unavailable.", "",
        "## Questions still not answered", "",
        "- Korean NAV and ownership mechanisms remain blocked by missing dated ownership histories and point-in-time valuation inputs.",
        "- Samsung payout delivery is one preparation step away: annual reports are local, but a reviewed DPS/policy/publication-date panel is not yet assembled.",
        "- Borrow fees, lendable inventory, KRX short positions, historical GDR parity, and true Korean bid/ask/depth remain unavailable.",
        "- No result in this batch validates a trading strategy or a stable fair-value anchor.", "",
    ]
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    parser.add_argument("--issuer-run", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    repo = Path.cwd()
    config_path = repo / args.config
    cfg = json.loads(config_path.read_text())
    paths = {k: repo / v["path"] for k, v in cfg["inputs"].items()}
    for name, item in cfg["inputs"].items():
        require(paths[name].is_file(), f"missing input {name}")
        require(digest(paths[name]) == item["sha256"], f"input hash mismatch {name}")

    annual, annual_diag, annual_summary = annual_supply(paths["annual_supply"], cfg["annual"])
    samsung, samsung_panel = samsung_adjustment(paths["samsung_raw"], paths["samsung_grid"], cfg["samsung_leg_adjustment"])
    tsmc, tsmc_panel, tsmc_audit = tsmc_discovery(paths["core_pair_panels"], cfg["tsmc_price_discovery"])
    events, doses = event_summary(repo / args.issuer_run)

    output = repo / args.output
    output.mkdir(parents=True, exist_ok=False)
    annual.to_csv(output / "annual_supply_regressions.csv", index=False)
    annual_diag.to_csv(output / "annual_rank_diagnostics.csv", index=False)
    samsung.to_csv(output / "samsung_leg_adjustment.csv", index=False)
    tsmc.to_csv(output / "tsmc_price_discovery.csv", index=False)
    events.to_csv(output / "issuer_event_windows.csv", index=False)
    doses.to_csv(output / "issuer_event_doses.csv", index=False)
    samsung_panel.to_csv(output / "samsung_adjustment_panel.csv", index=False)
    tsmc_panel.to_csv(output / "tsmc_timing_panel.csv", index=False)
    (output / "REPORT.md").write_text(report(annual, annual_diag, annual_summary, samsung, tsmc, tsmc_audit, events, doses))
    manifest = {"config": args.config, "config_sha256": digest(config_path), "code_sha256": digest(Path(__file__)),
                "inputs": cfg["inputs"], "annual_summary": annual_summary, "tsmc_audit": tsmc_audit,
                "scope": cfg["purpose"]}
    (output / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    for name, item in cfg["inputs"].items():
        require(digest(paths[name]) == item["sha256"], f"input changed {name}")
    print(json.dumps({"output": str(output), "annual_models": len(annual), "samsung_models": len(samsung),
                      "tsmc_models": len(tsmc), "event_windows": len(events)}, indent=2))


if __name__ == "__main__":
    main()
