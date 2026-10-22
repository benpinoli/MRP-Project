import math
import sys
import unittest
from datetime import date, timedelta
from pathlib import Path

import numpy as np

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"src"))
from samsung_research.descriptive import difference, rolling_std, volume_ratio, build_measures


class DescriptiveChecks(unittest.TestCase):
    def test_percentage_points_and_no_bridging(self):
        a=difference([10,11,np.nan,14,15])
        np.testing.assert_allclose(a,[np.nan,1,np.nan,np.nan,1],equal_nan=True)

    def test_sample_std_and_minimum_window(self):
        a=rolling_std([1,-1]*10,20)
        self.assertTrue(np.isnan(a[:19]).all())
        self.assertAlmostEqual(a[19],math.sqrt(20/19))

    def test_missing_window_never_compresses_and_no_lookahead(self):
        x=np.arange(45,dtype=float)
        x[20]=np.nan
        a=rolling_std(x)
        self.assertTrue(np.isnan(a[20:40]).all())
        self.assertTrue(math.isfinite(a[40]))
        np.testing.assert_allclose(a[:30],rolling_std(x[:30]),equal_nan=True)

    def test_volume_ratio_zero_missing_and_units(self):
        self.assertEqual(volume_ratio(200,1000),.2)
        self.assertEqual(volume_ratio(0,1000),0)
        for p,c in [(2,0),(None,2),(-2,3),(2,np.nan)]:
            self.assertTrue(math.isnan(volume_ratio(p,c)))

    def test_sensitivity_preserves_grid_and_masks_both_change_endpoints(self):
        dates=[]
        t=date(2020,1,1)
        while len(dates)<50:
            if t.weekday()<5:
                dates.append(t.isoformat())
            t+=timedelta(days=1)
        normalized=[]
        paired=[]
        for i,t in enumerate(dates):
            for j in ("common","preferred"):
                normalized.append(dict(datadate=t,class_name=j,price_eligible=True,prcstd="10",cshtrd="100",prccd="100"))
            paired.append(dict(datadate=t,discount_pct=10+i/10))
        diag=[dict(date=dates[10],review_flags="large_discount_change")]
        r,flags,annual=build_measures(normalized,paired,diag,[],dict(window_sessions=20))
        self.assertEqual([x["date"] for x in r["main"]],[x["date"] for x in r["sensitivity"]])
        self.assertTrue(math.isnan(r["sensitivity"][10]["discount_change_pp"]))
        self.assertTrue(math.isnan(r["sensitivity"][11]["discount_change_pp"]))
        self.assertTrue(math.isfinite(r["sensitivity"][12]["discount_change_pp"]))
        self.assertTrue(math.isnan(r["sensitivity"][30]["rolling_change_std_pp"]))
        self.assertTrue(math.isfinite(r["sensitivity"][31]["rolling_change_std_pp"]))
        self.assertEqual(annual[0]["observations"]-annual[1]["observations"],1)


if __name__=="__main__":
    unittest.main()
