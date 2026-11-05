import os,unittest
os.environ.setdefault('SAMSUNG_REPO',os.getcwd())
import numpy as np
import pandas as pd
from samsung_research.prediction_activity_range import activity_and_ranges,ridge
class ActivityChecks(unittest.TestCase):
    def test_trailing_surprise_and_valid_ranges(self):
        dates=pd.date_range('2020-01-01',periods=63).strftime('%Y-%m-%d');grid=pd.DataFrame({'date':dates,'volume_ratio':[1.]*60+[np.e**2,0,1.]})
        rows=[]
        for name in ('preferred','common'):
            for i,date in enumerate(dates):
                rows.append({'class_name':name,'datadate':date,'price_eligible':True,'prcld':'10','prchd':'20' if name=='preferred' else '10','prccd':'10'})
        rows[0]['prchd']='9';out=activity_and_ranges(grid,rows)
        self.assertTrue(np.isnan(out.activity_surprise.iloc[59]));self.assertAlmostEqual(out.activity_surprise.iloc[60],2.)
        self.assertTrue(np.isnan(out.activity_surprise.iloc[61]));self.assertTrue(np.isnan(out.activity_surprise.iloc[62]));self.assertTrue(np.isnan(out.relative_range.iloc[0]));self.assertAlmostEqual(out.relative_range.iloc[1],np.log(2))
    def test_fixed_calendar_flags(self):
        grid=pd.DataFrame({'date':['2016-03-24','2016-03-25','2016-12-26','2016-11-25'],'volume_ratio':[1.]*4})
        out=activity_and_ranges(grid,[])
        self.assertEqual(out.QE.tolist(),[0,1,1,0]);self.assertEqual(out.YE.tolist(),[0,0,1,0])
    def test_ridge(self):
        x=np.array([[1.],[2.],[3.]]);p,_=ridge(x,np.array([2.,4.,6.]),np.array([[4.]]),1);np.testing.assert_allclose(p,[7.])
if __name__=='__main__':unittest.main()
