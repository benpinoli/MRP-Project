"""Small synthetic checks for the remaining core-pair panel builder."""
import importlib.util
import sys
import unittest
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("core_pair_baselines", ROOT / "scripts/run_core_pair_baselines.py")
MODULE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


class CorePairBaselineChecks(unittest.TestCase):
    def test_changes_do_not_bridge_unusable_endpoint(self):
        panel = pd.DataFrame({"date": pd.date_range("2020-01-01", periods=4)})
        gap = pd.Series([0.0, 1.0, 9.0, 3.0])
        result = MODULE.add_changes(panel, pd.Series([True, True, False, True]), gap, gap / 100)
        self.assertAlmostEqual(result.dd_pp.iloc[1], 1.0)
        self.assertTrue(result.dd_pp.iloc[2:].isna().all())
        self.assertTrue(result.lag_gap.iloc[2:].isna().all())

    def test_compustat_adjustment_neutralizes_split(self):
        raw = pd.DataFrame({
            "gvkey": ["1", "1"], "iid": ["01W", "01W"], "conm": ["X", "X"], "curcdd": ["KRW", "KRW"],
            "date": pd.to_datetime(["2020-01-01", "2020-01-02"]), "prccd": [5000, 100], "ajexdi": [50, 1],
            "qunit": [1, 1], "cshtrd": [1, 1], "prcstd": [10, 10],
        })
        out = MODULE.global_leg(raw, {"gvkey": "1", "iid": "01W", "name": "X", "currency": "KRW"}, "x", 10)
        np.testing.assert_allclose(out.x_adjusted_close, [100, 100])
        self.assertTrue(out.x_usable.all())


if __name__ == "__main__":
    unittest.main()
