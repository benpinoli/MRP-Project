import os,unittest
os.environ.setdefault('SAMSUNG_REPO',os.getcwd())
import numpy as np
import pandas as pd
from samsung_research.prediction_external import prepare_source,align_source,ridge
class ExternalChecks(unittest.TestCase):
    def test_availability_and_valid_observation_lag(self):
        f=pd.DataFrame({'d':pd.date_range('2020-01-01',periods=12),'v':[1,2,3,None,4,5,6,7,8,9,10,10000]})
        s=prepare_source(f,'d','v','2020-01-01','2020-01-11','vix')
        a=align_source(['2020-01-12','2020-02-01'],s,'vix',2,7)
        self.assertEqual(a.vix_source_date.iloc[0],pd.Timestamp('2020-01-10'))
        self.assertEqual(a.vix_baseline_date.iloc[0],pd.Timestamp('2020-01-05'))
        self.assertAlmostEqual(a.vix_change5.iloc[0],np.log(9/4))
        self.assertTrue(pd.isna(a.vix_level.iloc[1]))
    def test_ridge_training_standardization(self):
        x=np.array([[1.],[2.],[3.]]);y=np.array([2.,4.,6.]);p,a=ridge(x,y,np.array([[4.]]),1)
        np.testing.assert_allclose(p,[7.]);np.testing.assert_allclose(a['mean'],[2.])
if __name__=='__main__':unittest.main()
