import os, unittest
os.environ.setdefault('SAMSUNG_REPO',os.getcwd())
import numpy as np
import pandas as pd
from samsung_research.prediction_diagnostics import training_thresholds, summary, classify
class DiagnosticChecks(unittest.TestCase):
    def test_maturity_and_prior_only_quantile(self):
        dates=pd.Series(pd.date_range('2020-01-01',periods=320)); grid=pd.DataFrame({'q':np.arange(320,dtype=float)})
        r=training_thresholds(grid,dates,[dates.iloc[300]],5,20).iloc[0]
        self.assertEqual(r.training_max_label_end,dates.iloc[299]); self.assertEqual(r.abs_y_p99,5)
        grid.loc[300:,'q']=100000
        r2=training_thresholds(grid,dates,[dates.iloc[300]],5,20).iloc[0]
        self.assertEqual(r2.abs_y_p99,5)
    def test_errors_and_bins(self):
        g=pd.DataFrame({'actual':[1.,-2.], 'prediction':[.5,0], 'z0':[0.,0.], 'a0':[1.,-1.], 'd1':[1.,2.], 'local':[1.,-1.], 'q':[10.,11.]})
        s=summary(g); self.assertAlmostEqual(s['model_mae'],1.25); self.assertAlmostEqual(s['bias_actual_minus_pred'],-.75); self.assertAlmostEqual(s['a0_mae'],.5)
        self.assertEqual(list(classify(pd.Series([0.,2.,4.]),pd.Series([1.]*3),pd.Series([3.]*3))),['low','middle','high'])
if __name__=='__main__': unittest.main()
