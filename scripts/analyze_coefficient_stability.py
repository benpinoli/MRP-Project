"""Bounded coefficient-stability follow-up for the frozen Samsung RG runs.

The reconciliation stage is metadata/data-mask work only.  Empirical fitting is
implemented in a separate stage so it can be run through Slurm.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import chi2, norm


PRIMARY_RUN = Path("runs/samsung/RG/20261103T010848_30613")
BASELINE_RUN = Path("runs/samsung/RG/20261103T010838_25471")
EP01_RUN = Path("runs/samsung/RG/20261026T131821Z_setup/EP01/20261026T131848_234484Z")
PLAN = Path("docs/regressions/COEFFICIENT_STABILITY_AGENT_PLAN.md")

WINDOWS = {
    "full": ("2005-01-03", "2026-10-20"),
    "2005_2014": ("2005-01-03", "2014-12-31"),
    "2015_2019": ("2015-01-01", "2019-12-31"),
    "2020_2026": ("2020-01-01", "2026-10-20"),
}

FACTOR_COLUMNS = [
    "F_USSLOWL_COUNTRY",
    "F_USSLOWL_BETA",
    "F_USSLOWL_VALUE",
    "F_USSLOWL_SIZE",
    "F_USSLOWL_MOMENTUM",
    "F_USSLOWL_LIQUIDTY",
    "F_USSLOWL_RESVOL",
    "F_USSLOWL_LEVERAGE",
    "F_USSLOWL_DIVYILD",
    "F_USSLOWL_PROFIT",
    "F_USSLOWL_SEMICOND",
]

MODEL_COLUMNS = {
    "B00": ("dd_pp", ["lag_discount"]),
    "B01": ("dd_pp", FACTOR_COLUMNS),
    "B02": ("dg", FACTOR_COLUMNS),
    "B03": ("dd_pp", ["lag_discount", *FACTOR_COLUMNS]),
    "B04": ("dd_pp", ["lag_discount", "lag_activity", *FACTOR_COLUMNS]),
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def json_write(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, indent=2, allow_nan=False) + "\n", encoding="utf-8")


def markdown_table(frame: pd.DataFrame) -> str:
    """Render a compact Markdown table without pandas' optional tabulate dependency."""
    display = frame.copy()
    display = display.fillna("").astype(str).map(lambda value: value.replace("|", "\\|").replace("\n", " "))
    header = "| " + " | ".join(display.columns) + " |"
    rule = "| " + " | ".join("---" for _ in display.columns) + " |"
    rows = ["| " + " | ".join(row) + " |" for row in display.to_numpy().tolist()]
    return "\n".join([header, rule, *rows])


def mask_hash(frame: pd.DataFrame, mask: pd.Series) -> str:
    dates = frame.loc[mask, "date"].astype(str).tolist()
    return hashlib.sha256(("\n".join(dates) + "\n").encode()).hexdigest()


def file_record(repo: Path, path: Path, *, required: bool, role: str) -> dict:
    full = repo / path
    return {
        "path": path.as_posix(),
        "role": role,
        "required_for_steps_1_3": required,
        "present": full.is_file(),
        "bytes": full.stat().st_size if full.is_file() else None,
        "sha256": sha256(full) if full.is_file() else None,
    }


def build_inventory(repo: Path, out: Path) -> dict:
    records = []
    specified = [
        (PLAN, True, "execution plan"),
        (Path("docs/regressions/B01_B04_RETROSPECTIVE_COEFFICIENT_TABLES.md"), False, "user summary named by plan"),
        (PRIMARY_RUN / "REPORT.md", True, "primary run report"),
        (PRIMARY_RUN / "coefficients.csv", True, "primary collected coefficients"),
        (PRIMARY_RUN / "status.json", True, "primary task status"),
        (PRIMARY_RUN / "tasks.json", True, "primary task map"),
        (PRIMARY_RUN / "prepared/panel.csv", True, "primary prepared design"),
        (PRIMARY_RUN / "prepared/alignment.csv", True, "factor alignment report"),
        (PRIMARY_RUN / "prepared/inputs.json", True, "primary input hashes"),
        (PRIMARY_RUN / "frozen/config.json", True, "primary frozen config"),
        (PRIMARY_RUN / "frozen/src/samsung_research/regressions.py", True, "primary frozen implementation"),
        (BASELINE_RUN / "REPORT.md", True, "B00 supporting report"),
        (BASELINE_RUN / "coefficients.csv", True, "B00 collected coefficients"),
        (BASELINE_RUN / "prepared/panel.csv", True, "B00 prepared design"),
        (EP01_RUN / "manifest.json", True, "EP01 manifest"),
        (EP01_RUN / "tables/measures_main.csv", True, "EP01 main grid and flags"),
        (EP01_RUN / "tables/measures_sensitivity.csv", True, "EP01 registered sensitivity"),
        (EP01_RUN / "provenance/source_inventory.json", True, "EP01 source inventory"),
        (Path("data/regression/raw/barra/factors.csv"), True, "retrospective US factor input"),
        (Path("configs/us_barra_retrospective_metadata.v1.json"), True, "retrospective factor metadata"),
        (Path("data/regression/staged/mechanisms.csv"), False, "optional M01-M04 mechanisms"),
        (Path("data/regression/metadata/mechanisms.json"), False, "optional mechanism provenance"),
        (Path("data/regression/metadata/factor_timing.csv"), False, "strict-timestamp factor timing"),
        (Path("data/regression/metadata/factor_calendar.csv"), False, "strict-timestamp factor calendar"),
        (Path("data/regression/metadata/sessions.csv"), False, "strict-timestamp Korean closes"),
        (Path("data/regression/metadata/barra.json"), False, "strict-timestamp Barra metadata"),
    ]
    for path, required, role in specified:
        records.append(file_record(repo, path, required=required, role=role))

    local_code = repo / "src/samsung_research/regressions.py"
    frozen_code = repo / PRIMARY_RUN / "frozen/src/samsung_research/regressions.py"
    primary_inputs = json.loads((repo / PRIMARY_RUN / "prepared/inputs.json").read_text())
    verified_hashes = []
    for path_text, expected in primary_inputs["sha256"].items():
        path = Path(path_text)
        actual = sha256(path) if path.is_file() else None
        verified_hashes.append({"path": str(path), "expected": expected, "actual": actual, "matches": actual == expected})
    panel_actual = sha256(repo / PRIMARY_RUN / "prepared/panel.csv")
    verified_hashes.append({
        "path": (PRIMARY_RUN / "prepared/panel.csv").as_posix(),
        "expected": primary_inputs["panel_sha256"],
        "actual": panel_actual,
        "matches": panel_actual == primary_inputs["panel_sha256"],
    })

    inventory = {
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "primary_source_run": PRIMARY_RUN.as_posix(),
        "supporting_baseline_run": BASELINE_RUN.as_posix(),
        "ep01_source_run": EP01_RUN.as_posix(),
        "join_rule": "retrospective preceding-US-session [previous Korean session date, current Korean session date)",
        "local_code_sha256": sha256(local_code),
        "frozen_code_sha256": sha256(frozen_code),
        "local_matches_frozen": sha256(local_code) == sha256(frozen_code),
        "files": records,
        "verified_source_hashes": verified_hashes,
        "reproducible_steps_1_3": all(r["present"] for r in records if r["required_for_steps_1_3"])
        and all(r["matches"] for r in verified_hashes),
        "known_missing_later_inputs": [
            "M01 relative spreads and float-adjusted turnover",
            "M02 retail participation and foreign flows",
            "M03 common borrow fees",
            "M04 class repurchase executions and incremental dividend entitlement",
            "strict availability/vintage timestamps required for a forecasting claim",
        ],
    }
    json_write(out / "inventory.json", inventory)
    return inventory


def reconcile(repo: Path, out: Path) -> pd.DataFrame:
    factor_panel = pd.read_csv(repo / PRIMARY_RUN / "prepared/panel.csv")
    baseline_panel = pd.read_csv(repo / BASELINE_RUN / "prepared/panel.csv")
    source = pd.read_csv(repo / EP01_RUN / "tables/measures_main.csv")
    observed = source.loc[source["observed_session"].astype(str).str.lower().eq("true")].copy().reset_index(drop=True)
    observed["grid_index"] = np.arange(len(observed))
    observed["previous_date"] = observed["date"].shift()
    flags = observed.loc[observed["flagged"].astype(str).str.lower().eq("true"), ["date", "grid_index", "flag_reasons"]].copy()
    flag_by_date = flags.set_index("date").to_dict("index")

    panel_for_model = {"B00": baseline_panel, "B01": factor_panel, "B02": factor_panel, "B03": factor_panel, "B04": factor_panel}
    summary_rows = []
    detail_rows = []
    for model_id, (outcome, columns) in MODEL_COLUMNS.items():
        panel = panel_for_model[model_id]
        for window_id, (start, end) in WINDOWS.items():
            by_variant = {}
            for variant in ("main", "sensitivity"):
                frame = panel.loc[panel["variant"].eq(variant)].copy()
                in_window = frame["date"].between(start, end)
                complete = frame[[outcome, *columns]].notna().all(axis=1)
                by_variant[variant] = (frame, in_window & complete)
            main_frame, main_mask = by_variant["main"]
            sens_frame, sens_mask = by_variant["sensitivity"]
            main_dates = set(main_frame.loc[main_mask, "date"])
            sens_dates = set(sens_frame.loc[sens_mask, "date"])
            main_only = sorted(main_dates - sens_dates)
            sens_only = sorted(sens_dates - main_dates)
            source_flag_dates = sorted(d for d in flag_by_date if start <= d <= end)
            summary_rows.append({
                "model_id": model_id,
                "window_id": window_id,
                "outcome": outcome,
                "regressors": ";".join(columns),
                "n_main": len(main_dates),
                "n_sensitivity": len(sens_dates),
                "main_minus_sensitivity": len(main_dates) - len(sens_dates),
                "main_only_rows": len(main_only),
                "sensitivity_only_rows": len(sens_only),
                "original_flagged_price_dates": len(source_flag_dates),
                "main_first_date": min(main_dates) if main_dates else "",
                "main_last_date": max(main_dates) if main_dates else "",
                "sensitivity_first_date": min(sens_dates) if sens_dates else "",
                "sensitivity_last_date": max(sens_dates) if sens_dates else "",
                "main_date_mask_sha256": mask_hash(main_frame, main_mask),
                "sensitivity_date_mask_sha256": mask_hash(sens_frame, sens_mask),
                "main_only_dates": ";".join(main_only),
                "sensitivity_only_dates": ";".join(sens_only),
                "flagged_price_dates": ";".join(source_flag_dates),
            })
            lookup = observed.set_index("date")
            for regression_date in main_only:
                row = lookup.loc[regression_date]
                related = []
                if regression_date in flag_by_date:
                    related.append((regression_date, "current_price", flag_by_date[regression_date]["flag_reasons"]))
                previous_date = row["previous_date"]
                if isinstance(previous_date, str) and previous_date in flag_by_date:
                    related.append((previous_date, "prior_price_difference_or_lag", flag_by_date[previous_date]["flag_reasons"]))
                if not related:
                    related.append(("", "unattributed_complete_case_difference", ""))
                for flag_date, relation, reason in related:
                    detail_rows.append({
                        "model_id": model_id,
                        "window_id": window_id,
                        "regression_date_lost": regression_date,
                        "regression_grid_index": int(row["grid_index"]),
                        "source_flagged_price_date": flag_date,
                        "propagation_relation": relation,
                        "source_flag_reason": reason,
                    })

    summary = pd.DataFrame(summary_rows)
    summary.to_csv(out / "sample_reconciliation.csv", index=False)
    pd.DataFrame(detail_rows).to_csv(out / "sample_loss_attribution.csv", index=False)
    flags.to_csv(out / "source_flagged_price_dates.csv", index=False)
    return summary


def write_ledger(out: Path, inventory: dict) -> None:
    missing_mechanisms = not (out.parents[3] / "data/regression/staged/mechanisms.csv").is_file()
    rows = [
        {
            "item": "inventory_and_hash_verification",
            "status": "completed" if inventory["reproducible_steps_1_3"] else "blocked",
            "evidence_path": "inventory.json",
            "evidence_sha256": sha256(out / "inventory.json"),
            "decision": "Use one primary B01-B04 run and the separate registered B00 run; do not merge arbitrary runs.",
            "blocker": "" if inventory["reproducible_steps_1_3"] else "Required source artifact/hash mismatch.",
            "next_action": "Exact sample reconciliation.",
        },
        {
            "item": "sample_reconciliation",
            "status": "completed",
            "evidence_path": "sample_reconciliation.csv;sample_loss_attribution.csv",
            "evidence_sha256": sha256(out / "sample_reconciliation.csv"),
            "decision": "Preserve original session grid and attribute losses to flagged source dates plus lag/difference propagation.",
            "blocker": "",
            "next_action": "Freeze influence candidates after the prespecified screen.",
        },
        {
            "item": "mechanism_blocks_M01_M04",
            "status": "blocked" if missing_mechanisms else "ready",
            "evidence_path": "inventory.json",
            "evidence_sha256": sha256(out / "inventory.json"),
            "decision": "Do not treat missing mechanisms as zero or as null results.",
            "blocker": "No staged mechanisms/provenance files." if missing_mechanisms else "",
            "next_action": "Continue steps 2-3 independently; produce exact mechanism coverage handoff.",
        },
        {
            "item": "state_interactions",
            "status": "blocked",
            "evidence_path": "inventory.json",
            "evidence_sha256": sha256(out / "inventory.json"),
            "decision": "Do not fit interactions without qualified state data and main effects.",
            "blocker": "No qualified spread, flow, or borrow-fee state series.",
            "next_action": "Revisit only after prioritized mechanism data qualify.",
        },
        {
            "item": "forecasting_evaluation",
            "status": "blocked",
            "evidence_path": "inventory.json",
            "evidence_sha256": sha256(out / "inventory.json"),
            "decision": "Do not reinterpret retrospective preceding-US-session joins as origin-safe forecasts.",
            "blocker": "Factor publication/vintage timing is explicitly unavailable.",
            "next_action": "Supply origin-safe availability/vintage metadata or limit future work to a labeled retrospective pseudo-OOS exercise.",
        },
    ]
    pd.DataFrame(rows).to_csv(out / "status_ledger.csv", index=False)


def prepared_design(panel: pd.DataFrame, model_id: str, window_id: str, variant: str) -> tuple[pd.DataFrame, str, list[str]]:
    outcome, columns = MODEL_COLUMNS[model_id]
    start, end = WINDOWS[window_id]
    selected = panel.loc[panel["variant"].eq(variant) & panel["date"].between(start, end)].copy()
    used = selected.dropna(subset=[outcome, *columns]).copy()
    return used, outcome, columns


def fit_hac(y: np.ndarray, x: np.ndarray, grid: np.ndarray, bandwidth: int) -> dict:
    """Stable OLS and original-session-grid Bartlett HAC covariance."""
    y = np.asarray(y, dtype=float)
    x = np.asarray(x, dtype=float)
    grid = np.asarray(grid, dtype=int)
    n, k = x.shape
    means = x[:, 1:].mean(axis=0)
    scales = x[:, 1:].std(axis=0)
    if n <= k or np.any(scales <= 0) or not np.isfinite(x).all() or not np.isfinite(y).all():
        raise ValueError("Invalid or unidentified design")
    z = np.column_stack([np.ones(n), (x[:, 1:] - means) / scales])
    q, r = np.linalg.qr(z, mode="reduced")
    if np.linalg.matrix_rank(r) < k:
        raise ValueError("Rank-deficient design")
    bz = np.linalg.solve(r, q.T @ y)
    residual = y - z @ bz
    transform = np.eye(k)
    transform[0, 1:] = -means / scales
    transform[1:, 1:] = np.diag(1 / scales)
    b = transform @ bz
    solve_r = np.linalg.solve(r, np.eye(k))
    bread_z = solve_r @ solve_r.T
    scores = np.zeros((grid[-1] - grid[0] + 1, k))
    scores[grid - grid[0]] = z * residual[:, None]
    meat = scores.T @ scores
    for lag in range(1, min(bandwidth, len(scores) - 1) + 1):
        cross = scores[lag:].T @ scores[:-lag]
        meat += (1 - lag / (bandwidth + 1)) * (cross + cross.T)
    cov_z = bread_z @ meat @ bread_z * n / (n - k)
    cov = transform @ cov_z @ transform.T
    sst = float(((y - y.mean()) ** 2).sum())
    ssr = float(residual @ residual)
    return {
        "coefficient": b,
        "covariance": cov,
        "std_error": np.sqrt(np.maximum(np.diag(cov), 0)),
        "residual": residual,
        "fitted": y - residual,
        "ssr": ssr,
        "r_squared": 1 - ssr / sst,
        "adjusted_r_squared": 1 - (1 - (1 - ssr / sst)) * (n - 1) / (n - k),
        "n": n,
        "k": k,
    }


def influence_diagnostics(y: np.ndarray, x: np.ndarray) -> dict:
    """Classical OLS influence quantities using QR and linear solves."""
    y = np.asarray(y, dtype=float)
    x = np.asarray(x, dtype=float)
    n, k = x.shape
    means = x[:, 1:].mean(axis=0)
    scales = x[:, 1:].std(axis=0)
    z = np.column_stack([np.ones(n), (x[:, 1:] - means) / scales])
    q, r = np.linalg.qr(z, mode="reduced")
    bz = np.linalg.solve(r, q.T @ y)
    residual = y - z @ bz
    leverage = np.sum(q * q, axis=1)
    sse = float(residual @ residual)
    mse = sse / (n - k)
    studentized = residual / np.sqrt(mse * np.maximum(1 - leverage, np.finfo(float).eps))
    cooks = studentized**2 * leverage / (k * np.maximum(1 - leverage, np.finfo(float).eps))
    transform = np.eye(k)
    transform[0, 1:] = -means / scales
    transform[1:, 1:] = np.diag(1 / scales)
    solve_r = np.linalg.solve(r, np.eye(k))
    c_z = solve_r @ solve_r.T
    dfbetas = np.empty((n, k))
    for i in range(n):
        one_minus_h = max(1 - leverage[i], np.finfo(float).eps)
        v = c_z @ z[i]
        delta = transform @ (v * residual[i] / one_minus_h)
        c_leave_z = c_z + np.outer(v, v) / one_minus_h
        c_leave = transform @ c_leave_z @ transform.T
        sse_leave = sse - residual[i] ** 2 / one_minus_h
        sigma2_leave = max(sse_leave / (n - k - 1), np.finfo(float).eps)
        dfbetas[i] = delta / np.sqrt(np.maximum(sigma2_leave * np.diag(c_leave), np.finfo(float).eps))
    return {
        "fitted": y - residual,
        "residual": residual,
        "leverage": leverage,
        "studentized_internal": studentized,
        "cooks_distance": cooks,
        "dfbetas": dfbetas,
    }


def group_session_dates(dates: list[str], date_to_grid: dict[str, int], max_gap: int = 2) -> list[list[str]]:
    ordered = sorted(set(dates), key=lambda d: date_to_grid[d])
    groups: list[list[str]] = []
    for date in ordered:
        if not groups or date_to_grid[date] - date_to_grid[groups[-1][-1]] > max_gap:
            groups.append([date])
        else:
            groups[-1].append(date)
    return groups


def run_influence_screen(repo: Path, out: Path, panel: pd.DataFrame, source: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    source_observed = source.loc[source["observed_session"].astype(str).str.lower().eq("true")].copy().reset_index(drop=True)
    source_observed["grid_index"] = np.arange(len(source_observed))
    source_flags = source_observed[["date", "flagged", "flag_reasons"]]
    screen_rows = []
    screen_models = ["B01", "B03"]
    screen_windows = ["2005_2014", "2015_2019", "2020_2026"]
    for model_id in screen_models:
        for window_id in screen_windows:
            used, outcome, columns = prepared_design(panel, model_id, window_id, "main")
            x = np.column_stack([np.ones(len(used)), used[columns].to_numpy(float)])
            diagnostics = influence_diagnostics(used[outcome].to_numpy(float), x)
            terms = ["intercept", *columns]
            joined = used[["date", "grid_index", outcome]].merge(source_flags, on="date", how="left", validate="one_to_one")
            joined["model_id"] = model_id
            joined["window_id"] = window_id
            joined["eligibility"] = "complete_main_design"
            joined["fitted"] = diagnostics["fitted"]
            joined["residual"] = diagnostics["residual"]
            joined["leverage"] = diagnostics["leverage"]
            joined["studentized_internal"] = diagnostics["studentized_internal"]
            joined["cooks_distance"] = diagnostics["cooks_distance"]
            joined["cooks_within_fit_percentile"] = joined["cooks_distance"].rank(method="max", pct=True)
            for j, term in enumerate(terms):
                joined[f"dfbetas__{term}"] = diagnostics["dfbetas"][:, j]
            target_terms = [term for term in ["lag_discount", "F_USSLOWL_BETA", "F_USSLOWL_MOMENTUM", "F_USSLOWL_LEVERAGE"] if term in terms]
            joined["max_abs_target_dfbetas"] = joined[[f"dfbetas__{term}" for term in target_terms]].abs().max(axis=1)
            joined["target_dfbetas_within_fit_percentile"] = joined["max_abs_target_dfbetas"].rank(method="max", pct=True)
            screen_rows.append(joined)
    screen = pd.concat(screen_rows, ignore_index=True)
    screen.to_csv(out / "influence_screen.csv", index=False)

    grid_map = source_observed.set_index("date")["grid_index"].astype(int).to_dict()
    loss = pd.read_csv(out / "sample_loss_attribution.csv")
    relevant_loss = loss.loc[loss["model_id"].isin(screen_models) & loss["source_flagged_price_date"].astype(str).ne("")]
    flagged_dates = sorted(set(relevant_loss["source_flagged_price_date"].dropna().astype(str)))
    flagged_groups = group_session_dates(flagged_dates, grid_map)

    rank_candidates = []
    for (_, _), fit in screen.groupby(["model_id", "window_id"], sort=True):
        rank_candidates.append(fit.nlargest(3, "cooks_distance"))
        rank_candidates.append(fit.nlargest(3, "max_abs_target_dfbetas"))
    ranked = pd.concat(rank_candidates, ignore_index=True)
    ranked["best_within_fit_percentile"] = ranked[["cooks_within_fit_percentile", "target_dfbetas_within_fit_percentile"]].max(axis=1)
    ranked = ranked.loc[~ranked["date"].isin(flagged_dates)]
    date_rank = ranked.groupby("date", as_index=False).agg(best_within_fit_percentile=("best_within_fit_percentile", "max"), grid_index=("grid_index", "first"))
    unflagged_groups = group_session_dates(date_rank["date"].tolist(), grid_map)
    unflagged = []
    date_rank_map = date_rank.set_index("date")["best_within_fit_percentile"].to_dict()
    for group in unflagged_groups:
        unflagged.append({"dates": group, "rank": max(date_rank_map[d] for d in group)})
    unflagged = sorted(unflagged, key=lambda x: (-x["rank"], x["dates"][0]))[:6]

    episodes = []
    for group in flagged_groups:
        episodes.append({"candidate_class": "source_flagged", "member_dates": group, "selection_rank": 1.0})
    for item in unflagged:
        episodes.append({"candidate_class": "influence_ranked_unflagged", "member_dates": item["dates"], "selection_rank": item["rank"]})
    episodes = episodes[:12]
    rows = []
    for number, episode in enumerate(episodes, 1):
        rows.append({
            "episode_id": f"E{number:02d}",
            "candidate_class": episode["candidate_class"],
            "member_dates": ";".join(episode["member_dates"]),
            "first_grid_index": min(grid_map[d] for d in episode["member_dates"]),
            "last_grid_index": max(grid_map[d] for d in episode["member_dates"]),
            "best_within_fit_percentile": episode["selection_rank"],
            "candidate_list_frozen": True,
        })
    candidates = pd.DataFrame(rows)
    candidates.to_csv(out / "episode_candidates.csv", index=False)
    return screen, candidates


def build_episode_audit(repo: Path, out: Path, panel: pd.DataFrame, source: pd.DataFrame, candidates: pd.DataFrame) -> pd.DataFrame:
    observed = source.loc[source["observed_session"].astype(str).str.lower().eq("true")].copy().reset_index(drop=True)
    observed["grid_index"] = np.arange(len(observed))
    observed["common_change"] = observed["common_raw_close"].pct_change(fill_method=None)
    observed["preferred_change"] = observed["preferred_raw_close"].pct_change(fill_method=None)
    observed["discount_change_recomputed_pp"] = observed["discount_pct"].diff()
    parsed = pd.to_datetime(observed["date"])
    observed["interval_calendar_days"] = parsed.diff().dt.days
    main_panel = panel.loc[panel["variant"].eq("main")].copy()
    alignment = pd.read_csv(repo / PRIMARY_RUN / "prepared/alignment.csv")
    alignment_summary = alignment.groupby("date", as_index=False).agg(
        aligned_factor_dates=("factor_date", lambda x: ";".join(str(v) for v in x if pd.notna(v) and str(v))),
        alignment_status=("status", lambda x: ";".join(sorted(set(map(str, x))))),
    )
    packet_rows = []
    for episode in candidates.itertuples(index=False):
        anchors = episode.member_dates.split(";")
        anchor_grids = [int(observed.loc[observed["date"].eq(d), "grid_index"].iloc[0]) for d in anchors]
        lower, upper = max(0, min(anchor_grids) - 2), min(len(observed) - 1, max(anchor_grids) + 2)
        packet = observed.loc[observed["grid_index"].between(lower, upper)].copy()
        packet.insert(0, "episode_id", episode.episode_id)
        packet["is_candidate_member"] = packet["date"].isin(anchors)
        packet = packet.merge(main_panel[["date", *FACTOR_COLUMNS]], on="date", how="left", validate="one_to_one")
        packet = packet.merge(alignment_summary, on="date", how="left", validate="one_to_one")
        packet["adjusted_prices_or_action_factors"] = "unavailable"
        packet["quote_status_fields"] = "unavailable"
        packet["source_row_ids"] = "unavailable"
        packet["corporate_action_dividend_records"] = "unavailable"
        packet_rows.append(packet)
    audit = pd.concat(packet_rows, ignore_index=True)
    audit.to_csv(out / "episode_packet.csv", index=False)

    audit_rows = []
    for episode in candidates.itertuples(index=False):
        subset = audit.loc[audit["episode_id"].eq(episode.episode_id) & audit["is_candidate_member"]]
        positive = bool((subset["common_raw_close"] > 0).all() and (subset["preferred_raw_close"] > 0).all())
        if episode.candidate_class == "source_flagged":
            status = "registered eligibility exclusion"
            confidence = "high"
            reason = "; ".join(sorted(set(subset["flag_reasons"].dropna().astype(str))))
        else:
            status = "unresolved"
            confidence = "low"
            reason = "Raw prices are positive and internally ratio-consistent; adjusted/action and quote-status evidence are unavailable."
        audit_rows.append({
            "episode_id": episode.episode_id,
            "dates": episode.member_dates,
            "candidate_class": episode.candidate_class,
            "triage_status": status,
            "evidence_confidence": confidence,
            "raw_price_positive": positive,
            "evidence": reason,
            "source_references": f"{EP01_RUN}/tables/measures_main.csv; {PRIMARY_RUN}/prepared/alignment.csv",
            "unavailable_evidence": "verified adjusted prices/action factors; quote-status fields; corporate-action/dividend records; source row IDs",
        })
    audit_table = pd.DataFrame(audit_rows)
    lines = [
        "# Fixed episode audit",
        "",
        "Candidate list frozen before external research. Classical influence is a screen, not a data-error probability.",
        "",
        markdown_table(audit_table),
        "",
        "Detailed ±2-session packets: [episode_packet.csv](episode_packet.csv). Overview: [episode_overview.png](episode_overview.png).",
    ]
    (out / "episode_audit.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(figsize=(12, 4.5))
    ax.plot(pd.to_datetime(observed["date"]), observed["discount_pct"], color="#244a73", linewidth=0.8)
    for episode in candidates.itertuples(index=False):
        color = "#b33b2e" if episode.candidate_class == "source_flagged" else "#d89b2b"
        for date in episode.member_dates.split(";"):
            ax.axvline(pd.Timestamp(date), color=color, alpha=0.7, linewidth=0.9)
    ax.set(title="Samsung common/preferred discount and frozen review episodes", ylabel="Discount (percentage points)", xlabel="Korean session")
    fig.tight_layout()
    fig.savefig(out / "episode_overview.png", dpi=160)
    plt.close(fig)
    return audit_table


def fit_frame(frame: pd.DataFrame, outcome: str, columns: list[str], bandwidth: int = 20) -> dict:
    x = np.column_stack([np.ones(len(frame)), frame[columns].to_numpy(float)])
    return fit_hac(frame[outcome].to_numpy(float), x, frame["grid_index"].to_numpy(int), bandwidth)


def run_sensitivity(out: Path, panel: pd.DataFrame, candidates: pd.DataFrame) -> tuple[pd.DataFrame, str]:
    loss = pd.read_csv(out / "sample_loss_attribution.csv")
    result_rows = []
    for model_id in ["B01", "B03"]:
        for window_id in ["2005_2014", "2015_2019", "2020_2026"]:
            main, outcome, columns = prepared_design(panel, model_id, window_id, "main")
            sensitivity, _, _ = prepared_design(panel, model_id, window_id, "sensitivity")
            original = fit_frame(main, outcome, columns, 20)
            terms = ["intercept", *columns]
            scenarios: list[tuple[str, pd.DataFrame, list[str]]] = [("source_main", main, []), ("registered_sensitivity", sensitivity, sorted(set(main.date) - set(sensitivity.date)))]
            combined_dates: set[str] = set()
            for episode in candidates.itertuples(index=False):
                members = episode.member_dates.split(";")
                if episode.candidate_class == "source_flagged":
                    exact = loss.loc[
                        loss["model_id"].eq(model_id)
                        & loss["window_id"].eq(window_id)
                        & loss["source_flagged_price_date"].astype(str).isin(members),
                        "regression_date_lost",
                    ].dropna().astype(str).tolist()
                else:
                    exact = [d for d in members if d in set(main["date"])]
                exact = sorted(set(exact))
                if exact:
                    combined_dates.update(exact)
                    scenarios.append((f"omit_{episode.episode_id}", main.loc[~main["date"].isin(exact)].copy(), exact))
            if combined_dates:
                scenarios.append(("omit_all_selected", main.loc[~main["date"].isin(combined_dates)].copy(), sorted(combined_dates)))
            for scenario, frame, omitted in scenarios:
                fit = original if scenario == "source_main" else fit_frame(frame, outcome, columns, 20)
                for j, term in enumerate(terms):
                    base = original["coefficient"][j]
                    coefficient = fit["coefficient"][j]
                    result_rows.append({
                        "model_id": model_id,
                        "window_id": window_id,
                        "variant_scenario": scenario,
                        "hac_lag": 20,
                        "term": term,
                        "n": fit["n"],
                        "coefficient": coefficient,
                        "std_error": fit["std_error"][j],
                        "original_coefficient": base,
                        "signed_change": coefficient - base,
                        "change_over_original_hac_se": (coefficient - base) / original["std_error"][j],
                        "sign_change": bool(np.sign(coefficient) != np.sign(base)),
                        "r_squared": fit["r_squared"],
                        "original_r_squared": original["r_squared"],
                        "omitted_regression_dates": ";".join(omitted),
                        "descriptive_selected_deletion": scenario.startswith("omit_"),
                    })
    sensitivity_results = pd.DataFrame(result_rows)
    sensitivity_results.to_csv(out / "influence_sensitivity.csv", index=False)
    target = sensitivity_results.loc[
        sensitivity_results["term"].isin(["lag_discount", "F_USSLOWL_BETA", "F_USSLOWL_MOMENTUM", "F_USSLOWL_LEVERAGE"])
        & ~sensitivity_results["variant_scenario"].eq("source_main")
    ]
    # A sign flip around zero is not a substantive reversal.  Treat the fixed
    # batch as sensitive only when a targeted change reaches one original HAC
    # standard error; preserve all sign changes in the artifact for review.
    material = bool((target["change_over_original_hac_se"].abs() >= 1).any())
    conclusion = "sensitive to a few observations" if material else "robust to reviewed episodes"
    return sensitivity_results, conclusion


def wald_test(fit: dict, restriction: np.ndarray, value: np.ndarray | None = None) -> tuple[float, int, float]:
    r = np.asarray(restriction, float)
    target = np.zeros(r.shape[0]) if value is None else np.asarray(value, float)
    diff = r @ fit["coefficient"] - target
    rcov = r @ fit["covariance"] @ r.T
    solved = np.linalg.solve(rcov, diff)
    statistic = float(diff @ solved)
    df = r.shape[0]
    return statistic, df, float(chi2.sf(statistic, df))


def common_sample_comparisons(out: Path, panel: pd.DataFrame) -> pd.DataFrame:
    comparisons = [
        ("B00_vs_B03", ["lag_discount"], ["lag_discount", *FACTOR_COLUMNS], FACTOR_COLUMNS),
        ("B01_vs_B03", FACTOR_COLUMNS, ["lag_discount", *FACTOR_COLUMNS], ["lag_discount"]),
        ("B03_vs_B04", ["lag_discount", *FACTOR_COLUMNS], ["lag_discount", "lag_activity", *FACTOR_COLUMNS], ["lag_activity"]),
    ]
    rows = []
    for variant in ["main", "sensitivity"]:
        variant_panel = panel.loc[panel["variant"].eq(variant)].copy()
        for window_id, (start, end) in WINDOWS.items():
            selected = variant_panel.loc[variant_panel["date"].between(start, end)].copy()
            for name, restricted_columns, unrestricted_columns, added in comparisons:
                used = selected.dropna(subset=["dd_pp", *unrestricted_columns]).copy()
                restricted = fit_frame(used, "dd_pp", restricted_columns, 20)
                unrestricted = fit_frame(used, "dd_pp", unrestricted_columns, 20)
                terms = ["intercept", *unrestricted_columns]
                r = np.zeros((len(added), len(terms)))
                for i, term in enumerate(added):
                    r[i, terms.index(term)] = 1
                statistic, df, p = wald_test(unrestricted, r)
                rows.append({
                    "comparison": name,
                    "variant": variant,
                    "window_id": window_id,
                    "n": len(used),
                    "first_date": used["date"].iloc[0],
                    "last_date": used["date"].iloc[-1],
                    "date_mask_sha256": mask_hash(used, pd.Series(True, index=used.index)),
                    "restricted_terms": ";".join(restricted_columns),
                    "added_terms": ";".join(added),
                    "restricted_r_squared": restricted["r_squared"],
                    "unrestricted_r_squared": unrestricted["r_squared"],
                    "restricted_adjusted_r_squared": restricted["adjusted_r_squared"],
                    "unrestricted_adjusted_r_squared": unrestricted["adjusted_r_squared"],
                    "partial_r_squared": (restricted["ssr"] - unrestricted["ssr"]) / restricted["ssr"],
                    "hac_lag": 20,
                    "wald_chi2": statistic,
                    "wald_df": df,
                    "wald_p_value": p,
                })
    result = pd.DataFrame(rows)
    result.to_csv(out / "common_sample_comparisons.csv", index=False)
    return result


def bh_adjust(p_values: np.ndarray) -> np.ndarray:
    p_values = np.asarray(p_values, float)
    order = np.argsort(p_values)
    ranked = p_values[order] * len(p_values) / np.arange(1, len(p_values) + 1)
    adjusted_sorted = np.minimum.accumulate(ranked[::-1])[::-1].clip(0, 1)
    adjusted = np.empty(len(p_values))
    adjusted[order] = adjusted_sorted
    return adjusted


def stability_tests(out: Path, panel: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    used, outcome, base_columns = prepared_design(panel, "B03", "full", "main")
    period = np.select(
        [used["date"].between(*WINDOWS["2005_2014"]), used["date"].between(*WINDOWS["2015_2019"]), used["date"].between(*WINDOWS["2020_2026"])],
        ["2005_2014", "2015_2019", "2020_2026"], default="outside")
    used = used.assign(period=period)
    used = used.loc[used["period"].ne("outside")].copy()
    design = used[base_columns].copy()
    terms = ["intercept", *base_columns]
    for later in ["2015_2019", "2020_2026"]:
        dummy = used["period"].eq(later).astype(float)
        design[f"period_{later}"] = dummy
        terms.append(f"period_{later}")
        for column in base_columns:
            name = f"{column}__x__{later}"
            design[name] = used[column] * dummy
            terms.append(name)
    x = np.column_stack([np.ones(len(used)), design.to_numpy(float)])
    fit = fit_hac(used[outcome].to_numpy(float), x, used["grid_index"].to_numpy(int), 20)
    if len(terms) != len(fit["coefficient"]):
        raise RuntimeError("Pooled stability term map mismatch")

    tests = []
    factor_interactions = [f"{factor}__x__{period_id}" for period_id in ["2015_2019", "2020_2026"] for factor in FACTOR_COLUMNS]
    lag_interactions = [f"lag_discount__x__{period_id}" for period_id in ["2015_2019", "2020_2026"]]
    declared = [
        ("primary_joint_factor_slope_equality", factor_interactions, "primary"),
        ("primary_joint_lag_discount_equality", lag_interactions, "primary"),
    ]
    for factor in ["F_USSLOWL_BETA", "F_USSLOWL_MOMENTUM", "F_USSLOWL_LEVERAGE"]:
        declared.append((f"secondary_{factor}_equality", [f"{factor}__x__2015_2019", f"{factor}__x__2020_2026"], "secondary"))
    for name, restricted_terms, family_role in declared:
        r = np.zeros((len(restricted_terms), len(terms)))
        for i, term in enumerate(restricted_terms):
            r[i, terms.index(term)] = 1
        statistic, df, p = wald_test(fit, r)
        tests.append({"test_id": name, "test_role": family_role, "contrast": ";".join(restricted_terms), "estimate": np.nan, "std_error": np.nan, "ci_lower": np.nan, "ci_upper": np.nan, "wald_chi2": statistic, "wald_df": df, "p_value": p})

    target_slopes = ["lag_discount", "F_USSLOWL_BETA", "F_USSLOWL_MOMENTUM", "F_USSLOWL_LEVERAGE"]
    coefficient_rows = []
    for target in target_slopes:
        base_index = terms.index(target)
        vectors = {}
        for period_id in ["2005_2014", "2015_2019", "2020_2026"]:
            vector = np.zeros(len(terms))
            vector[base_index] = 1
            if period_id != "2005_2014":
                vector[terms.index(f"{target}__x__{period_id}")] = 1
            vectors[period_id] = vector
            estimate = float(vector @ fit["coefficient"])
            se = float(np.sqrt(vector @ fit["covariance"] @ vector))
            coefficient_rows.append({"term": target, "period": period_id, "estimate": estimate, "std_error": se, "ci_lower": estimate - 1.95996398454 * se, "ci_upper": estimate + 1.95996398454 * se, "n_total_pooled": len(used), "hac_lag": 20})
        for left, right in [("2005_2014", "2015_2019"), ("2005_2014", "2020_2026"), ("2015_2019", "2020_2026")]:
            vector = vectors[right] - vectors[left]
            estimate = float(vector @ fit["coefficient"])
            se = float(np.sqrt(vector @ fit["covariance"] @ vector))
            statistic = (estimate / se) ** 2
            tests.append({
                "test_id": f"secondary_pairwise_{target}_{right}_minus_{left}",
                "test_role": "secondary",
                "contrast": f"{right} - {left}",
                "estimate": estimate,
                "std_error": se,
                "ci_lower": estimate - 1.95996398454 * se,
                "ci_upper": estimate + 1.95996398454 * se,
                "wald_chi2": statistic,
                "wald_df": 1,
                "p_value": float(chi2.sf(statistic, 1)),
            })
    test_frame = pd.DataFrame(tests)
    test_frame["multiplicity_family"] = "coefficient_stability_followup_v1"
    test_frame["q_value_bh"] = bh_adjust(test_frame["p_value"].to_numpy())
    test_frame["sample_date_mask_sha256"] = mask_hash(used, pd.Series(True, index=used.index))
    test_frame.to_csv(out / "stability_tests.csv", index=False)
    coefficient_frame = pd.DataFrame(coefficient_rows)
    coefficient_frame.to_csv(out / "stability_coefficients.csv", index=False)
    return test_frame, coefficient_frame


def stationarity_sensitivity(out: Path, source: pd.DataFrame) -> pd.DataFrame:
    observed = source.loc[source["observed_session"].astype(str).str.lower().eq("true"), ["date", "discount_pct"]].copy().reset_index(drop=True)
    q = observed["discount_pct"].astype(float)
    rows = []
    for deterministic in ["constant", "constant_trend"]:
        for lag in [0, 5, 20]:
            dq = q.diff()
            frame = pd.DataFrame({"dq": dq, "q_lag": q.shift(1)})
            for j in range(1, lag + 1):
                frame[f"dq_lag_{j}"] = dq.shift(j)
            frame = frame.dropna()
            columns = ["q_lag", *[f"dq_lag_{j}" for j in range(1, lag + 1)]]
            x_parts = [np.ones(len(frame))]
            if deterministic == "constant_trend":
                x_parts.append(np.arange(len(frame), dtype=float))
            x_parts.extend(frame[c].to_numpy(float) for c in columns)
            x = np.column_stack(x_parts)
            b, _, _, _ = np.linalg.lstsq(x, frame["dq"].to_numpy(float), rcond=None)
            residual = frame["dq"].to_numpy(float) - x @ b
            sigma2 = residual @ residual / (len(frame) - x.shape[1])
            q_lag_position = 2 if deterministic == "constant_trend" else 1
            qx, rx = np.linalg.qr(x, mode="reduced")
            solve_r = np.linalg.solve(rx, np.eye(rx.shape[0]))
            covariance = sigma2 * solve_r @ solve_r.T
            statistic = b[q_lag_position] / np.sqrt(covariance[q_lag_position, q_lag_position])
            rows.append({"test": "ADF", "deterministic": deterministic, "lag_or_bandwidth": lag, "n": len(frame), "statistic": statistic, "p_value": np.nan, "interpretation_note": "MacKinnon p-value unavailable; compare statistics across declared deterministic/lag sensitivities, not as a standalone equilibrium proof."})
    for deterministic in ["constant", "constant_trend"]:
        grid = np.arange(len(q), dtype=float)
        x_full = np.ones((len(q), 1)) if deterministic == "constant" else np.column_stack([np.ones(len(q)), grid])
        complete = q.notna().to_numpy()
        b = np.linalg.lstsq(x_full[complete], q.loc[complete].to_numpy(float), rcond=None)[0]
        # Keep the original session grid. Missing observations contribute zero
        # residual score instead of compressing the HAC/KPSS lag distance.
        residual = np.zeros(len(q), dtype=float)
        residual[complete] = q.loc[complete].to_numpy(float) - x_full[complete] @ b
        cumulative = np.cumsum(residual)
        for bandwidth in [5, 20, 60]:
            lrv = float(residual @ residual / complete.sum())
            for lag in range(1, bandwidth + 1):
                covariance = float(residual[lag:] @ residual[:-lag] / complete.sum())
                lrv += 2 * (1 - lag / (bandwidth + 1)) * covariance
            statistic = float(cumulative @ cumulative / (complete.sum() ** 2 * lrv))
            rows.append({"test": "KPSS", "deterministic": deterministic, "lag_or_bandwidth": bandwidth, "n": int(complete.sum()), "statistic": statistic, "p_value": np.nan, "interpretation_note": "Descriptive KPSS bandwidth sensitivity on the original session grid with zero scores at missing levels; conventional critical-value inference must account for deterministic specification."})
    result = pd.DataFrame(rows)
    result.to_csv(out / "stationarity_sensitivity.csv", index=False)
    return result


def mechanism_coverage(out: Path) -> pd.DataFrame:
    definitions = {
        "M01": "spread_diff;log_turnover_ratio",
        "M02": "retail_weight_diff;foreign_flow_diff",
        "M03": "common_borrow_fee",
        "M04": "buyback_diff;incremental_dividend",
        "L01": "retail_weight_diff;log_turnover_ratio;incremental_dividend",
    }
    rows = []
    for model_id, fields in definitions.items():
        rows.append({
            "model_id": model_id,
            "required_fields": fields,
            "field_definition_source": "docs/regressions/FACTORS.md",
            "class_identifiers": "not supplied",
            "units": "defined in FACTORS.md; no observed file supplied",
            "start_date": "",
            "end_date": "",
            "missingness": "100% unavailable",
            "availability_lag": "unavailable",
            "revision_status": "unavailable",
            "independent_release_event_count": "unavailable",
            "licensing_source": "unavailable",
            "status": "blocked_missing_input_and_provenance",
            "why_it_matters": "Required to test the registered mechanism rather than proxying it with raw volume or a policy dummy.",
        })
    result = pd.DataFrame(rows)
    result.to_csv(out / "mechanism_coverage.csv", index=False)
    return result


def update_ledger_after_empirical(out: Path, audit_conclusion: str) -> None:
    ledger = pd.read_csv(out / "status_ledger.csv")
    additions = [
        ("influence_screen_and_episode_audit", "completed", "influence_screen.csv;episode_candidates.csv;episode_audit.md", audit_conclusion, "", "Stop date hunt after bounded sensitivity batch."),
        ("bounded_influence_sensitivity", "completed", "influence_sensitivity.csv", audit_conclusion, "", "No further deletions absent a newly established systematic error."),
        ("common_sample_comparisons", "completed", "common_sample_comparisons.csv", "Interpret incremental fit only on identical masks.", "", "Report partial R2 and HAC Wald tests."),
        ("formal_period_stability", "completed", "stability_tests.csv;stability_coefficients.csv", "Use registered periods; no exhaustive break search.", "", "Report joint and declared secondary tests with separate BH family."),
        ("discount_stationarity", "completed", "stationarity_sensitivity.csv", "Do not infer stable equilibrium from lag coefficient alone.", "", "Treat tests as specification sensitivities."),
        ("mechanism_coverage", "completed_blocker_documented", "mechanism_coverage.csv", "No mechanism was empirically tested.", "Mechanism data/provenance absent.", "Highest-value input is qualified M01/M02 data."),
    ]
    replacement_items = {item for item, *_ in additions}
    ledger = ledger.loc[~ledger["item"].isin(replacement_items)].copy()
    for item, status, evidence, decision, blocker, next_action in additions:
        first_path = evidence.split(";")[0]
        ledger.loc[len(ledger)] = {
            "item": item,
            "status": status,
            "evidence_path": evidence,
            "evidence_sha256": sha256(out / first_path),
            "decision": decision,
            "blocker": blocker,
            "next_action": next_action,
        }
    ledger.to_csv(out / "status_ledger.csv", index=False)


def shortlisted_hac_robustness(out: Path, panel: pd.DataFrame) -> pd.DataFrame:
    rows = []
    main = panel.loc[panel["variant"].eq("main") & panel["date"].between(*WINDOWS["full"])].copy()
    comparisons = [
        ("B00_vs_B03", ["lag_discount"], ["lag_discount", *FACTOR_COLUMNS], FACTOR_COLUMNS),
        ("B01_vs_B03", FACTOR_COLUMNS, ["lag_discount", *FACTOR_COLUMNS], ["lag_discount"]),
        ("B03_vs_B04", ["lag_discount", *FACTOR_COLUMNS], ["lag_discount", "lag_activity", *FACTOR_COLUMNS], ["lag_activity"]),
    ]
    for name, restricted_columns, unrestricted_columns, added in comparisons:
        used = main.dropna(subset=["dd_pp", *unrestricted_columns]).copy()
        for bandwidth in [5, 20, 60]:
            unrestricted = fit_frame(used, "dd_pp", unrestricted_columns, bandwidth)
            terms = ["intercept", *unrestricted_columns]
            r = np.zeros((len(added), len(terms)))
            for i, term in enumerate(added):
                r[i, terms.index(term)] = 1
            statistic, df, p = wald_test(unrestricted, r)
            rows.append({"result_family": "full_main_common_sample", "result_id": name, "hac_lag": bandwidth, "wald_chi2": statistic, "wald_df": df, "p_value": p, "date_mask_sha256": mask_hash(used, pd.Series(True, index=used.index))})

    used, outcome, base_columns = prepared_design(panel, "B03", "full", "main")
    period = np.select(
        [used["date"].between(*WINDOWS["2005_2014"]), used["date"].between(*WINDOWS["2015_2019"]), used["date"].between(*WINDOWS["2020_2026"])],
        ["2005_2014", "2015_2019", "2020_2026"], default="outside")
    used = used.assign(period=period).loc[lambda x: x["period"].ne("outside")].copy()
    design = used[base_columns].copy()
    terms = ["intercept", *base_columns]
    for later in ["2015_2019", "2020_2026"]:
        dummy = used["period"].eq(later).astype(float)
        design[f"period_{later}"] = dummy
        terms.append(f"period_{later}")
        for column in base_columns:
            interaction = f"{column}__x__{later}"
            design[interaction] = used[column] * dummy
            terms.append(interaction)
    x = np.column_stack([np.ones(len(used)), design.to_numpy(float)])
    restrictions = {
        "primary_joint_factor_slope_equality": [f"{factor}__x__{period_id}" for period_id in ["2015_2019", "2020_2026"] for factor in FACTOR_COLUMNS],
        "primary_joint_lag_discount_equality": [f"lag_discount__x__{period_id}" for period_id in ["2015_2019", "2020_2026"]],
    }
    for bandwidth in [5, 20, 60]:
        fit = fit_hac(used[outcome].to_numpy(float), x, used["grid_index"].to_numpy(int), bandwidth)
        for result_id, restricted_terms in restrictions.items():
            r = np.zeros((len(restricted_terms), len(terms)))
            for i, term in enumerate(restricted_terms):
                r[i, terms.index(term)] = 1
            statistic, df, p = wald_test(fit, r)
            rows.append({"result_family": "primary_period_stability", "result_id": result_id, "hac_lag": bandwidth, "wald_chi2": statistic, "wald_df": df, "p_value": p, "date_mask_sha256": mask_hash(used, pd.Series(True, index=used.index))})
    result = pd.DataFrame(rows)
    result.to_csv(out / "shortlisted_hac_robustness.csv", index=False)
    return result


def write_report(out: Path, sensitivity: pd.DataFrame, audit_conclusion: str, comparisons: pd.DataFrame, tests: pd.DataFrame, candidates: pd.DataFrame) -> None:
    target = sensitivity.loc[
        sensitivity["term"].isin(["lag_discount", "F_USSLOWL_BETA", "F_USSLOWL_MOMENTUM", "F_USSLOWL_LEVERAGE"])
        & ~sensitivity["variant_scenario"].eq("source_main")
    ]
    largest = target.iloc[target["change_over_original_hac_se"].abs().argmax()]
    primary = tests.loc[tests["test_role"].eq("primary"), ["test_id", "wald_chi2", "wald_df", "p_value", "q_value_bh"]]
    main_full = comparisons.loc[comparisons["variant"].eq("main") & comparisons["window_id"].eq("full"), ["comparison", "n", "partial_r_squared", "wald_p_value"]]
    lines = [
        "# Samsung coefficient stability follow-up",
        "",
        f"Audit stopping decision: **{audit_conclusion}**.",
        "",
        "## Completed",
        "",
        f"The frozen screen contains six fits (B01/B03 × three registered periods) and {len(candidates)} frozen episodes. The largest targeted deletion/sample change was "
        f"{largest['change_over_original_hac_se']:.3f} original HAC standard errors for {largest['model_id']} {largest['window_id']} "
        f"{largest['term']} under `{largest['variant_scenario']}`.",
        "",
        "Full-sample common-mask comparisons (HAC 20):",
        "",
        markdown_table(main_full),
        "",
        "Registered-period primary stability tests (separate follow-up BH family):",
        "",
        markdown_table(primary),
        "",
        "## Blocked or deferred",
        "",
        "M01–M04/L01 are blocked because no qualified mechanism observations or provenance were supplied. State interactions are therefore blocked. Forecasting is blocked as a claim because factor publication/vintage timing is explicitly unavailable; no retrospective explanatory fit is relabeled as a forecast.",
        "",
        "## Artifacts",
        "",
        "[Inventory](inventory.json) · [Ledger](status_ledger.csv) · [Sample reconciliation](sample_reconciliation.csv) · "
        "[Influence screen](influence_screen.csv) · [Frozen candidates](episode_candidates.csv) · [Episode audit](episode_audit.md) · "
        "[Sensitivity](influence_sensitivity.csv) · [Common samples](common_sample_comparisons.csv) · "
        "[Stability tests](stability_tests.csv) · [Mechanism coverage](mechanism_coverage.csv)",
        "",
        "Reconstruction: use `.venv-rg/bin/python scripts/analyze_coefficient_stability.py empirical --out "
        f"{out.relative_to(Path.cwd()).as_posix()}` inside the recorded Slurm environment. Source inputs are hash-verified in `inventory.json`.",
    ]
    (out / "REPORT.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def run_empirical(repo: Path, out: Path) -> None:
    required = [out / "inventory.json", out / "sample_reconciliation.csv", out / "status_ledger.csv"]
    if not all(path.is_file() for path in required):
        raise SystemExit("Run the reconciliation stage first")
    panel = pd.read_csv(repo / PRIMARY_RUN / "prepared/panel.csv")
    source = pd.read_csv(repo / EP01_RUN / "tables/measures_main.csv")
    screen, candidates = run_influence_screen(repo, out, panel, source)
    build_episode_audit(repo, out, panel, source, candidates)
    sensitivity, audit_conclusion = run_sensitivity(out, panel, candidates)
    comparisons = common_sample_comparisons(out, panel)
    tests, _ = stability_tests(out, panel)
    shortlisted_hac_robustness(out, panel)
    stationarity_sensitivity(out, source)
    mechanism_coverage(out)
    json_write(out / "analysis_snapshot.json", {
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "analysis_script_sha256": sha256(repo / "scripts/analyze_coefficient_stability.py"),
        "plan_sha256": sha256(repo / PLAN),
        "primary_panel_sha256": sha256(repo / PRIMARY_RUN / "prepared/panel.csv"),
        "screen_formulae": {
            "leverage": "diag(Q Q') from reduced QR of the standardized design",
            "internally_studentized_residual": "e_i / sqrt(MSE * (1-h_i))",
            "cooks_distance": "r_i^2 * h_i / (k * (1-h_i))",
            "dfbetas": "(b_full-b_leave_i) / sqrt(sigma2_leave_i * diag((X_leave_i'X_leave_i)^-1)); computed by QR solves and rank-one deletion updates",
        },
        "central_inference": "Bartlett Newey-West HAC 20 on original session grid",
        "multiplicity_family": "coefficient_stability_followup_v1; separate from prior submission BH values",
        "audit_stopping_decision": audit_conclusion,
        "external_searches": 0,
        "external_source_opens": 0,
    })
    update_ledger_after_empirical(out, audit_conclusion)
    write_report(out, sensitivity, audit_conclusion, comparisons, tests, candidates)
    print(json.dumps({"screen_rows": len(screen), "episodes": len(candidates), "audit_conclusion": audit_conclusion, "comparisons": len(comparisons), "stability_tests": len(tests)}, indent=2))


def run_selftest() -> None:
    rng = np.random.default_rng(20261103)
    n = 120
    x = np.column_stack([np.ones(n), rng.normal(size=n), rng.normal(size=n)])
    y = x @ np.array([0.4, -0.8, 1.2]) + rng.normal(scale=0.3, size=n)
    diagnostics = influence_diagnostics(y, x)
    for i in [0, 17, 91]:
        keep = np.arange(n) != i
        b_full = np.linalg.lstsq(x, y, rcond=None)[0]
        b_leave = np.linalg.lstsq(x[keep], y[keep], rcond=None)[0]
        c_leave = np.linalg.solve(x[keep].T @ x[keep], np.eye(x.shape[1]))
        residual_leave = y[keep] - x[keep] @ b_leave
        sigma2_leave = residual_leave @ residual_leave / (keep.sum() - x.shape[1])
        direct = (b_full - b_leave) / np.sqrt(sigma2_leave * np.diag(c_leave))
        np.testing.assert_allclose(diagnostics["dfbetas"][i], direct, rtol=1e-9, atol=1e-9)
    grid = np.arange(n)
    fit = fit_hac(y, x, grid, 20)
    r = np.zeros((2, 3)); r[0, 1] = 1; r[1, 2] = 1
    statistic, df, p = wald_test(fit, r)
    assert statistic > 0 and df == 2 and 0 <= p <= 1
    dates = [f"2026-01-{day:02d}" for day in range(1, 11)]
    mapping = {date: i for i, date in enumerate(dates)}
    assert group_session_dates([dates[1], dates[3], dates[7]], mapping) == [[dates[1], dates[3]], [dates[7]]]
    print("synthetic coefficient-stability checks passed")


def run_reconciliation(repo: Path, out: Path) -> None:
    if any(out.iterdir()):
        raise SystemExit(f"Exclusive output directory is not empty: {out}")
    inventory = build_inventory(repo, out)
    if not inventory["reproducible_steps_1_3"]:
        raise SystemExit("Required source artifacts failed inventory/hash validation")
    summary = reconcile(repo, out)
    write_ledger(out, inventory)
    focus = summary.loc[summary["model_id"].isin(["B01", "B03", "B04"]),
                        ["model_id", "window_id", "n_main", "n_sensitivity", "main_minus_sensitivity"]]
    print(focus.to_string(index=False))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("stage", choices=["reconcile", "selftest", "empirical"])
    parser.add_argument("--repo", type=Path, default=Path.cwd())
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    repo = args.repo.resolve()
    out = args.out if args.out.is_absolute() else repo / args.out
    if args.stage == "reconcile":
        run_reconciliation(repo, out)
    elif args.stage == "selftest":
        run_selftest()
    else:
        run_empirical(repo, out)


if __name__ == "__main__":
    main()
