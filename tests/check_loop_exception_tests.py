"""Small synthetic checks for the LOOP-exception panel logic."""
import importlib.util
import sys
import unittest
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("loop_tests", ROOT / "scripts/run_loop_exception_tests.py")
MODULE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


class LoopExceptionChecks(unittest.TestCase):
    def test_action_flag_uses_vendor_price_discrepancy(self):
        raw = pd.DataFrame({"barrid": ["x"] * 3, "date": pd.date_range("2020-01-01", periods=3),
                            "price": [100.0, 50.0, 51.0], "return": [np.nan, 0.0, 2.0]})
        result = MODULE.add_action_flags(raw, 3.0)
        self.assertFalse(result.action_flag.iloc[0])
        self.assertTrue(result.action_flag.iloc[1])
        self.assertFalse(result.action_flag.iloc[2])

    def test_pair_panel_masks_action_boundary_without_editing_prices(self):
        dates = pd.date_range("2020-01-01", periods=3)
        rows = []
        for barrid, prices, flags in (("l", [100, 50, 51], [False, True, False]),
                                      ("r", [10, 10, 10], [False, False, False])):
            for date, price, flag in zip(dates, prices, flags):
                rows.append({"date": date, "barrid": barrid, "price": price, "return": 0.0,
                             "daily_volume": 1.0, "bid_ask_spread": .01, "market_cap": 100.0,
                             "action_flag": flag})
        panel, audit = MODULE.share_panel(pd.DataFrame(rows), {"id": "p", "left": "l", "right": "r", "left_units_per_right": 1})
        self.assertEqual(panel.left_price.tolist(), [100, 50, 51])
        self.assertTrue(pd.isna(panel.d_gap_pp.iloc[1]))
        self.assertEqual(audit["action_boundaries_masked"], 1)


if __name__ == "__main__":
    unittest.main()
