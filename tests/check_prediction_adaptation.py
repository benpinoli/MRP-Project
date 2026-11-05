import os,unittest
os.environ.setdefault('SAMSUNG_REPO',os.getcwd())
import numpy as np
import pandas as pd
from samsung_research.prediction_adaptation import train_indices,fit
class AdaptationChecks(unittest.TestCase):
    def test_756_is_grid_rows_and_label_maturity(self):
        q=pd.Series(np.arange(1000,dtype=float));q.iloc[300]=np.nan
        mask=train_indices(q,q,900,20,756); idx=np.flatnonzero(mask)
        self.assertEqual(idx[0],144);self.assertLess(idx[-1]+20,900);self.assertFalse(mask[300]);self.assertFalse(mask[280]);self.assertLess(mask.sum(),756)
    def test_ols_only_uses_matured_data(self):
        q=pd.Series(np.arange(400,dtype=float)); d=q.diff()
        beta,mask=fit(q,d,300,5,minimum=20);self.assertTrue(np.allclose(beta[0]+beta[1],5))
        q.iloc[300:]=100000; beta2,mask2=fit(q,q.diff(),300,5,minimum=20)
        np.testing.assert_allclose(beta,beta2);np.testing.assert_array_equal(mask,mask2)
if __name__=='__main__':unittest.main()
