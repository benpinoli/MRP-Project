import os,unittest
os.environ.setdefault('SAMSUNG_REPO',os.getcwd())
import numpy as np
import pandas as pd
from samsung_research.long_horizon_supply import annual_volume,normalize_counts,combine
class SupplyTests(unittest.TestCase):
 def test_split_volume_and_coverage(self):
  days=['2018-04-27','2018-05-04','2018-05-08'];rows=[]
  for name in ('common','preferred'):
   rows.extend([{'class_name':name,'datadate':days[0],'price_eligible':True,'cshtrd':'2'},{'class_name':name,'datadate':days[1],'price_eligible':True,'cshtrd':'100'},{'class_name':name,'datadate':days[2],'price_eligible':False,'cshtrd':'0'}])
  v=annual_volume(rows,days).iloc[0];self.assertEqual(v.common_annual_volume_postsplit_shares,200);self.assertEqual(v.common_valid_volume_rows,2);self.assertAlmostEqual(v.common_volume_coverage,2/3)
 def test_counts_and_gaps(self):
  base={'period_end':'2017-12-31','source_url':'x','source_page':'1','status':'ok','conflict_flags':[],'publication_status':'unknown','share_basis':'pre','issued_common':100,'treasury_common':20,'non_treasury_common':80,'issued_preferred':50,'treasury_preferred':10,'non_treasury_preferred':40}
  c=normalize_counts({'rows':[base]});self.assertEqual(c.non_treasury_common_postsplit.iloc[0],4000)
  v=pd.DataFrame({'year':[2017,2018,2019],'proxy_sessions':[10]*3,'preferred_volume_coverage':[1]*3,'common_volume_coverage':[1]*3,'preferred_annual_volume_postsplit_shares':[200]*3,'common_annual_volume_postsplit_shares':[400]*3});a=pd.DataFrame({'year':[2017,2018,2019],'qualified_months':[12]*3,'mean_monthly_q':[30.,20.,10.]});z=combine(v,c,a);self.assertFalse(z.joint_eligible.iloc[1]);self.assertTrue(np.isnan(z.change_preferred_to_common_nontreasury.iloc[2]))
if __name__=='__main__':unittest.main()
