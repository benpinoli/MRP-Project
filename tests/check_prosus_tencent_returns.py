#!/usr/bin/env python3
"""Focused validations for conversion, action boundaries, stale quotes, intervals and masks."""
import importlib.util
import json
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("pt", ROOT / "scripts/analyze_prosus_tencent_returns.py")
pt = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(pt)


cfg = pt.read_config(ROOT / "configs/prosus_tencent_return_regressions.v1.json")
bundle = ROOT / cfg["bundle_root"]
fx = pt.exact_fx_panel(bundle)

# ECB orientation: HKD/local-per-EUR times USD-per-EUR.
d = pd.Series(pd.to_datetime(["2026-09-30"]))
converted = pt.usd_value(pd.Series([100.0]), "HKD", d, fx).iloc[0]
expected = 100.0 / fx.loc[d.iloc[0], "HKD"] * fx.loc[d.iloc[0], "USD"]
assert np.isclose(converted, expected)

stocks, exclusions, identities = pt.security_returns(bundle, cfg, fx)
assert set(stocks) == {"prosus", "tencent", "naspers"}
assert all(len(frame) > 1500 for frame in stocks.values())

# Stale PRCSTD endpoints and adjustment/split boundaries cannot enter returns.
assert not exclusions.loc[exclusions.exclusion_reason.eq("prcstd_endpoint_not_10"), "usable"].any()
assert not exclusions.loc[exclusions.exclusion_reason.isin(["ajexdi_changed", "split_marker"]), "usable"].any()
assert exclusions.exclusion_reason.eq("prcstd_endpoint_not_10").any()

# Every retained relationship row uses exactly identical interval endpoints and one common C mask.
samples, _, audit = pt.build_relationship_samples(bundle, cfg)
for rid, frame in samples.items():
    assert frame[["start_date", "end_date"]].notna().all().all()
    assert (frame.start_date < frame.end_date).all()
    assert not frame.duplicated(["start_date", "end_date"]).any()
    assert frame[["dependent_excess_return"] + cfg["designs"]["C"]].notna().all().all()
    assert audit["attrition"][rid]["common_model_sample"] == len(frame)

# The regional RF series must be identical before one is used for excess returns.
assert audit["factors"]["rf_max_abs_difference"] <= 1e-12

# Config is frozen against trading/NAV work and includes declared event boundaries.
assert "no NAV" in cfg["purpose"] and "no" in cfg["purpose"].lower()
dates = {event["date"] for event in cfg["sensitivities"]["events"]}
assert {"2022-01-20", "2023-01-05", "2023-09-13", "2023-09-14", "2025-10-01"}.issubset(dates)
print(json.dumps({"status": "passed", "relationships": {k: len(v) for k, v in samples.items()}, "identities": identities}, indent=2, default=str))
