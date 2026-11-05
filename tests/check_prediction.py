import unittest
import numpy as np
import pandas as pd
from samsung_research.prediction import features, fit_predict, generate

class PredictionChecks(unittest.TestCase):
    def test_grid_and_strict_trailing_windows(self):
        f=pd.DataFrame({'discount_pct':[10.,11.,np.nan,13.,14.,15.], 'volume_ratio':[1.]*6})
        x=features(f)
        self.assertTrue(np.isnan(x.d1.iloc[3])); self.assertTrue(np.isnan(x.d5.iloc[5]))
        self.assertEqual(x.d1.iloc[4],1.)
    def test_ridge_training_scaling_and_arithmetic(self):
        x=np.array([[1.],[2.],[3.]])
        np.testing.assert_allclose(fit_predict(x,np.array([2.,4.,6.]),np.array([[4.]]),None),[8.])
        np.testing.assert_allclose(fit_predict(x,np.array([2.,4.,6.]),np.array([[4.]]),1),[7.])
    def test_maturity_and_fold_end(self):
        n=100; dates=pd.bdate_range('2014-11-03',periods=n)
        f=pd.DataFrame({'date':dates.strftime('%Y-%m-%d'),'discount_pct':np.arange(n,dtype=float),'volume_ratio':np.ones(n),'flagged':False})
        cfg={'validation_folds':[['2015-01-01','2015-02-13']], 'test_start':'2015-02-14','horizons':[5], 'families':{'Z0':[],'A0':['q']},'alphas':[1], 'minimum_training':1}
        p,audits=generate(f,cfg,'validation'); a=p[p.family=='A0']
        self.assertTrue(audits); self.assertIn('coefficients',audits[0])
        self.assertFalse(a.empty); self.assertTrue((a.train_label_end < a.origin).all()); self.assertTrue((p.target_date <= '2015-02-13').all())
        self.assertTrue((p.actual == 5).all()); self.assertTrue((p[p.family=='Z0'].prediction == 0).all())
if __name__=='__main__': unittest.main()
