"""Single-pair explanatory OLS pipeline. No database access or fitting on import."""
from __future__ import annotations

import hashlib
import importlib.metadata
import json
import platform
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import norm


def read_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def write_json(path, value):
    Path(path).write_text(json.dumps(value, indent=2, allow_nan=False) + "\n", encoding="utf-8")


def digest(path):
    h = hashlib.sha256()
    with Path(path).open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def resolve(repo, path):
    p = Path(path)
    return p if p.is_absolute() else Path(repo) / p


def dated_csv(path):
    df = pd.read_csv(path)
    if "date" not in df or df.date.isna().any() or df.date.duplicated().any():
        raise ValueError(f"Missing/duplicate dates: {path}")
    parsed = pd.to_datetime(df.date, format="%Y-%m-%d", errors="raise")
    if not (parsed.dt.strftime("%Y-%m-%d") == df.date).all():
        raise ValueError(f"Dates must be ISO YYYY-MM-DD: {path}")
    return df.sort_values("date").reset_index(drop=True)


def utc_column(series):
    # Reject timezone-naive values rather than assuming UTC.
    for x in series:
        if pd.isna(x) or datetime.fromisoformat(str(x).replace("Z", "+00:00")).tzinfo is None:
            raise ValueError("Every timestamp needs an explicit timezone offset")
    return pd.to_datetime(series, utc=True, errors="raise")


def numeric(series):
    a = pd.to_numeric(series, errors="raise").astype(float)
    if np.isinf(a).any():
        raise ValueError("Infinite numeric input")
    return a


def boolean(series):
    mapped = series.astype(str).str.lower().map({"true": True, "false": False})
    if mapped.isna().any():
        raise ValueError("Expected explicit True/False")
    return mapped.astype(bool)


def align_factors(sessions, factors, timing, names, scale):
    """End-time bins; never use a future available row, carry or zero-fill."""
    ends = utc_column(timing.period_end_utc)
    avail = utc_column(timing.available_at_utc)
    if (avail < ends).any() or not ends.is_monotonic_increasing or ends.duplicated().any():
        raise ValueError("Factor end/availability timestamps inconsistent")
    if factors.date.tolist() != timing.date.tolist():
        raise ValueError("Factor timing dates differ from factor rows")
    closes = utc_column(sessions.close_utc)
    if not closes.is_monotonic_increasing or closes.duplicated().any():
        raise ValueError("Korean close timestamps must strictly increase")
    values = factors[names].apply(numeric) * scale
    output = pd.DataFrame(np.nan, index=sessions.index, columns=["F_" + x for x in names])
    mappings = []
    for i in range(1, len(sessions)):
        selected = (ends > closes.iloc[i - 1]) & (ends <= closes.iloc[i])
        if not selected.any():
            mappings.append(dict(date=sessions.date.iloc[i], factor_date="", status="empty_bin"))
            continue
        for pos in np.flatnonzero(selected):
            mappings.append(dict(date=sessions.date.iloc[i], factor_date=factors.date.iloc[pos],
                                 status="available" if avail.iloc[pos] <= closes.iloc[i] else "late",
                                 period_end_utc=ends.iloc[pos].isoformat(),
                                 available_at_utc=avail.iloc[pos].isoformat()))
        if (avail[selected] <= closes.iloc[i]).all():
            # min_count prevents a partly missing multi-row bin from being accepted.
            block = values.loc[selected]
            output.iloc[i] = block.sum(min_count=len(block)).to_numpy()
    return output, pd.DataFrame(mappings)


def outcomes(frame):
    q = numeric(frame.discount_pct)
    c, p = numeric(frame.common_raw_close), numeric(frame.preferred_raw_close)
    valid = q.notna()
    if ((c[valid] <= 0) | (p[valid] <= 0)).any():
        raise ValueError("Nonpositive eligible price")
    np.testing.assert_allclose(q[valid], 100 * (1 - p[valid] / c[valid]), atol=1e-9)
    g = -np.log1p(-q / 100)
    volume_ratio = numeric(frame.volume_ratio)
    activity = np.log(volume_ratio.where(volume_ratio > 0))
    return pd.DataFrame({"dd_pp": q.diff(), "dg": g.diff(), "lag_discount": q.shift(),
                         "lag_activity": activity.shift()})


def tasks(config):
    return [dict(model=m, variant=v, window=w, hac=h)
            for m in config["models"] for v in ["main", "sensitivity"]
            for w in config["windows"] for h in config["hac_lags"]]


def readiness(repo, config):
    required = ["factors", "factor_timing", "factor_calendar", "sessions", "barra_metadata"]
    paths = {k: resolve(repo, config["inputs"][k]) for k in required}
    pack = resolve(repo, config["inputs"]["ep01_run"])
    paths.update({"ep01_" + x: pack / x for x in ["manifest.json", "tables/measures_main.csv",
                 "tables/measures_sensitivity.csv", "provenance/source_inventory.json"]})
    return {"status": "files_present_metadata_not_yet_validated" if all(p.is_file() for p in paths.values()) else "blocked",
            "missing": [str(p) for p in paths.values() if not p.is_file()],
            "task_count": len(tasks(config)), "empirical_models_run": False}


def prepare(repo, run, config):
    run = Path(run)
    out = run / "prepared"
    out.mkdir(exist_ok=False)
    check = readiness(repo, config)
    write_json(out / "readiness.json", check)
    if check["missing"]:
        raise ValueError("Required input files missing; see prepared/readiness.json")
    paths = {k: resolve(repo, v) for k, v in config["inputs"].items() if k != "ep01_run"}
    pack = resolve(repo, config["inputs"]["ep01_run"])
    manifest = read_json(pack / "manifest.json")
    if any(manifest.get(k) != config["expected_raw_sha256"] for k in ["input_sha256_before", "input_sha256_after"]):
        raise ValueError("EP01 manifest raw-source hash mismatch")
    expected = {x["path"]: x["sha256"] for x in manifest["outputs"]}
    used = [pack / "manifest.json"]
    for name in ["tables/measures_main.csv", "tables/measures_sensitivity.csv", "provenance/source_inventory.json"]:
        if digest(pack / name) != expected[name]:
            raise ValueError(f"EP01 hash mismatch: {name}")
        used.append(pack / name)
    inventory = read_json(pack / "provenance/source_inventory.json")
    if not any(x.get("sha256") == config["expected_raw_sha256"] for x in inventory["sources"]):
        raise ValueError("EP01 inventory does not contain registered raw hash")
    used.extend(p for p in paths.values() if p.is_file())
    hashes = {str(p): digest(p) for p in used}
    meta = read_json(paths["barra_metadata"])
    needed = ["model_id", "geography", "currency", "vintage", "units", "timing_source", "session_source",
              "calendar_source", "calendar_start", "calendar_end", "currency_justification"]
    if any(not meta.get(k) for k in needed) or meta.get("reviewed") is not True:
        raise ValueError("Complete and review Barra metadata before preparing")
    if meta["geography"] not in ["Korea", "global_with_Korea", "US_sensitivity"]:
        raise ValueError("Unsupported geography label")
    if (any(n.startswith("USSLOWL_") for n in config["factor_names"]) or meta["geography"] == "US_sensitivity") and meta.get("allow_us_sensitivity") is not True:
        raise ValueError("US factors require explicit sensitivity acknowledgement")
    if meta["units"] not in ["percent", "decimal"]:
        raise ValueError("Factor units must be percent or decimal")
    factors = dated_csv(paths["factors"])
    timing = dated_csv(paths["factor_timing"])
    calendar = dated_csv(paths["factor_calendar"])
    if factors.date.tolist() != calendar.date.tolist():
        raise ValueError("Factor dates differ from independently expected source calendar")
    if not len(calendar) or calendar.date.min() < meta["calendar_start"] or calendar.date.max() > meta["calendar_end"]:
        raise ValueError("Factor calendar outside declared coverage")
    sessions = dated_csv(paths["sessions"])
    main = dated_csv(pack / "tables/measures_main.csv")
    sensitivity = dated_csv(pack / "tables/measures_sensitivity.csv")
    if main.date.tolist() != sensitivity.date.tolist():
        raise ValueError("EP01 variants have different grids")
    session_mask = boolean(main.observed_session)
    if main.loc[session_mask, "date"].tolist() != sessions.date.tolist():
        raise ValueError("Session timestamp grid differs from EP01 proxy grid")
    if meta["calendar_start"] > sessions.date.iloc[0] or meta["calendar_end"] < sessions.date.iloc[-1]:
        raise ValueError("Factor calendar coverage must span the Korean sample")
    aligned, mapping = align_factors(sessions, factors, timing, config["factor_names"],
                                     .01 if meta["units"] == "percent" else 1.)
    mechanism = None
    if paths["mechanisms"].exists():
        mechanism = dated_csv(paths["mechanisms"])
        mechanism_meta = read_json(paths["mechanisms_metadata"])
        for column in mechanism.columns.drop("date"):
            if column not in config["mechanism_columns"]:
                raise ValueError(f"Unregistered mechanism: {column}")
            spec = mechanism_meta.get("columns", {}).get(column, {})
            if spec.get("available_by_close_reviewed") is not True or any(not spec.get(k) for k in ["formula", "unit", "source", "vintage_policy"]):
                raise ValueError(f"Missing mechanism provenance: {column}")
            mechanism[column] = numeric(mechanism[column])
        mechanism = sessions[["date"]].merge(mechanism, on="date", how="left", validate="one_to_one")
    panels = []
    for variant, frame in [("main", main), ("sensitivity", sensitivity)]:
        frame = frame.loc[session_mask].reset_index(drop=True)
        panel = pd.concat([sessions[["date"]], outcomes(frame), aligned], axis=1)
        panel["variant"] = variant
        panel["grid_index"] = np.arange(len(panel))
        if mechanism is not None:
            for column in mechanism.columns.drop("date"):
                # Mask flagged observations BEFORE lagging in the sensitivity.
                x = mechanism[column].copy()
                if variant == "sensitivity":
                    x = x.mask(boolean(frame.flagged))
                panel["lag_" + column] = x.shift()
        panels.append(panel)
    panel = pd.concat(panels, ignore_index=True)
    panel.to_csv(out / "panel.csv", index=False)
    mapping.to_csv(out / "alignment.csv", index=False)
    for p, before in hashes.items():
        if digest(p) != before:
            raise ValueError(f"Input changed during preparation: {p}")
    write_json(out / "inputs.json", {"sha256": hashes, "panel_sha256": digest(out / "panel.csv"),
               "ep01_run_id": manifest["run_id"], "barra": meta})
    write_json(run / "tasks.json", tasks(config))
    write_json(out / "readiness.json", {"status": "prepared_not_estimated", "rows_per_variant": len(sessions),
               "complete_rows_by_column": panel.groupby("variant").count().to_dict(),
               "alignment_status": mapping.status.value_counts().to_dict(), "empirical_models_run": False})


def fit_ols(y, x, grid, bandwidth, minimum=252, observations_per_parameter=20, max_condition=1e8):
    """OLS with Bartlett HAC score products at original-grid session distances."""
    y, x, grid = np.asarray(y, float), np.asarray(x, float), np.asarray(grid, int)
    n, k = x.shape
    if n < max(minimum, observations_per_parameter * k):
        raise ValueError(f"Insufficient observations: n={n}, k={k}")
    if not np.isfinite(x).all() or not np.isfinite(y).all() or len(np.unique(grid)) != n:
        raise ValueError("Nonfinite design or duplicate session grid")
    if (np.diff(grid) <= 0).any():
        raise ValueError("Grid must strictly increase")
    std = x[:, 1:].std(axis=0)
    if (std <= 0).any():
        raise ValueError("Constant regressor (beyond intercept)")
    z = np.column_stack([np.ones(n), (x[:, 1:] - x[:, 1:].mean(0)) / std])
    singular = np.linalg.svd(z, compute_uv=False)
    rank = np.linalg.matrix_rank(z)
    condition = singular[0] / singular[-1]
    if rank < k or condition > max_condition:
        raise ValueError(f"Unidentified/ill-conditioned design: rank={rank}/{k}, condition={condition}")
    # Stable scaled solve; map coefficients/covariance back to original units.
    transform = np.eye(k)
    transform[0, 1:] = -x[:, 1:].mean(0) / std
    transform[1:, 1:] = np.diag(1 / std)
    b_z = np.linalg.lstsq(z, y, rcond=None)[0]
    b = transform @ b_z
    residual = y - z @ b_z
    scores = np.zeros((grid[-1] - grid[0] + 1, k))
    scores[grid - grid[0]] = z * residual[:, None]
    meat = scores.T @ scores
    for lag in range(1, min(bandwidth, len(scores) - 1) + 1):
        cross = scores[lag:].T @ scores[:-lag]
        meat += (1 - lag / (bandwidth + 1)) * (cross + cross.T)
    bread = np.linalg.inv(z.T @ z)
    cov = transform @ (bread @ meat @ bread * n / (n - k)) @ transform.T
    se = np.sqrt(np.maximum(np.diag(cov), 0))
    if (se <= 0).any():
        raise ValueError("Degenerate inference: zero standard error")
    p = 2 * norm.sf(abs(b / se))
    sst = ((y - y.mean()) ** 2).sum()
    if sst <= 0:
        raise ValueError("Constant outcome")
    r2 = 1 - residual @ residual / sst
    vif = []
    for j in range(1, k):
        other = np.delete(z, j, axis=1)
        err = z[:, j] - other @ np.linalg.lstsq(other, z[:, j], rcond=None)[0]
        vif.append(float((z[:, j] @ z[:, j]) / (err @ err)))
    adjacent = np.diff(grid) == 1
    ac = float(np.corrcoef(residual[:-1][adjacent], residual[1:][adjacent])[0, 1]) if adjacent.sum() > 2 else None
    diagnostics = dict(n=n, k=k, n_per_k=n / k, rank=int(rank), standardized_condition=float(condition),
                       singular_values=singular.tolist(), vif=vif, r_squared=float(r2),
                       adjusted_r_squared=float(1 - (1-r2)*(n-1)/(n-k)), residual_lag1=ac)
    return b, se, p, residual, diagnostics


def fit_task(run, index, config):
    run = Path(run)
    task = read_json(run / "tasks.json")[index]
    out = run / "results" / f"task_{index:05d}"
    out.mkdir(parents=True, exist_ok=False)
    result = {"task_index": index, **task, "status": "failed"}
    try:
        panel_path = run / "prepared/panel.csv"
        if digest(panel_path) != read_json(run / "prepared/inputs.json")["panel_sha256"]:
            raise RuntimeError("Prepared panel hash changed")
        frame = pd.read_csv(panel_path)
        frame = frame.loc[frame.variant.eq(task["variant"])].copy()
        model, window = task["model"], task["window"]
        columns = model["columns"] + (["F_" + x for x in config["factor_names"]] if model["barra"] else [])
        if model.get("interaction"):
            a, b = model["interaction"]
            if a in frame and b in frame:
                frame["interaction"] = frame[a] * frame[b]
            columns = columns + ["interaction"]
        missing = [x for x in columns if x not in frame]
        if missing:
            result.update(status="blocked", reason="Missing columns: " + ", ".join(missing))
            return
        selected = frame.loc[frame.date.between(window["start"], window["end"])].copy()
        used = selected.dropna(subset=[model["outcome"]] + columns)
        try:
            b, se, p, residual, diagnostics = fit_ols(used[model["outcome"]],
                np.column_stack([np.ones(len(used)), used[columns].to_numpy()]), used.grid_index,
                task["hac"], config["min_observations"], config["observations_per_parameter"], config["max_condition"])
        except ValueError as exc:
            result.update(status="blocked", reason=str(exc))
            return
        pd.DataFrame(dict(term=["intercept"] + columns, coefficient=b, std_error=se, p_value=p,
                          ci_lower=b-1.95996398454*se, ci_upper=b+1.95996398454*se)).to_csv(out / "coefficients.csv", index=False)
        pd.DataFrame(dict(date=used.date, grid_index=used.grid_index, actual=used[model["outcome"]],
                          fitted=used[model["outcome"]]-residual, residual=residual)).to_csv(out / "residuals.csv", index=False)
        result.update(status="estimated", diagnostics=diagnostics, first_date=used.date.iloc[0],
                      last_date=used.date.iloc[-1], excluded_rows=len(selected)-len(used),
                      interpretation="Exploratory association; identical-sample nested refits still required")
    except Exception as exc:
        result.update(status="failed", reason=f"{type(exc).__name__}: {exc}")
        raise
    finally:
        write_json(out / "result.json", result)


def collect(run):
    run = Path(run)
    expected = read_json(run / "tasks.json")
    statuses, coefficients = [], []
    for i, task in enumerate(expected):
        folder = run / "results" / f"task_{i:05d}"
        record = read_json(folder / "result.json") if (folder / "result.json").exists() else dict(task_index=i, **task, status="missing")
        statuses.append(record)
        if record["status"] == "estimated":
            coef = pd.read_csv(folder / "coefficients.csv")
            coef["task_index"] = i
            coef["model_id"] = task["model"]["id"]
            coefficients.append(coef)
    if coefficients:
        table = pd.concat(coefficients, ignore_index=True)
        table["q_bh_exploratory"] = np.nan
        mask = table.term.ne("intercept")
        p = table.loc[mask, "p_value"].to_numpy()
        if len(p):
            order = np.argsort(p)
            corrected = np.minimum.accumulate((p[order] * len(p) / np.arange(1, len(p)+1))[::-1])[::-1].clip(0, 1)
            q = np.empty(len(p))
            q[order] = corrected
            table.loc[mask, "q_bh_exploratory"] = q
        table.to_csv(run / "coefficients.csv", index=False)
    write_json(run / "status.json", statuses)
    counts = {s: sum(r["status"] == s for r in statuses) for s in ["estimated", "blocked", "failed", "missing"]}
    lines = ["# Samsung RG submission report", "", json.dumps(counts), "",
             "Exploratory associations only. Blocked models are not null findings. See frozen/docs/regressions for methodology.", "",
             "[Input/timing audit](prepared/readiness.json) · [Alignment](prepared/alignment.csv) · [Status](status.json)", "",
             "| Task | Model | Variant / window / HAC | Status | Detail |", "|---|---|---|---|---|"]
    for r in statuses:
        lines.append(f"| {r['task_index']} | {r['model']['id']} | {r['variant']} / {r['window']['id']} / {r['hac']} | {r['status']} | {r.get('reason', 'Review task diagnostics and residuals')} |")
    (run / "REPORT.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    return counts


def freeze(repo, run, config_path):
    """Exclusive snapshot used by Slurm; no data or environment secrets copied."""
    repo, run = Path(repo), Path(run)
    run.mkdir(parents=True, exist_ok=False)
    frozen = run / "frozen"
    for name in ["src/samsung_research", "scripts", "slurm", "docs/regressions", "methodology"]:
        shutil.copytree(repo / name, frozen / name, ignore=shutil.ignore_patterns("__pycache__", "cluster.env.sh"))
    shutil.copy2(config_path, frozen / "config.json")
    shutil.copy2(repo / "research/regression-requirements.lock", frozen / "regression-requirements.lock")
    code_hashes = {p.relative_to(frozen).as_posix(): digest(p) for p in frozen.rglob("*") if p.is_file()}
    revision = subprocess.run(["git", "rev-parse", "HEAD"], cwd=repo, capture_output=True, text=True)
    dirty = subprocess.run(["git", "status", "--porcelain"], cwd=repo, capture_output=True, text=True)
    packages = sorted(f"{d.metadata['Name']}=={d.version}" for d in importlib.metadata.distributions())
    write_json(run / "snapshot.json", dict(created_utc=datetime.now(timezone.utc).isoformat(),
               python=sys.version, platform=platform.platform(), revision=revision.stdout.strip(),
               dirty_files=dirty.stdout.splitlines(), packages=packages, files=code_hashes))
    return run
