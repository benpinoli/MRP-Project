import os,unittest
os.environ.setdefault('SAMSUNG_REPO',os.getcwd())
import numpy as np
import pandas as pd
from samsung_research.long_horizon_map import monthly_grid,quarterly_grid,changes,state_runs
class LongHorizonTests(unittest.TestCase):
 def test_mean_of_ratios_and_coverage(self):
  f=pd.DataFrame({'date':['2020-01-02','2020-01-03','2020-03-02'],'observed_session':[True]*3,'flagged':[False]*3,'discount_pct':[50.,0.,20.],'preferred_raw_close':[50.,200.,80.],'common_raw_close':[100.,200.,100.]})
  m=monthly_grid(f,minimum=1,fraction=.8,last_complete='2020-03');self.assertEqual(m.loc['2020-01','mean_q'],25.);self.assertNotAlmostEqual(m.loc['2020-01','mean_q'],100*(1-125/150));self.assertFalse(m.loc['2020-02','qualified']);self.assertTrue(np.isnan(quarterly_grid(m).quarter_mean.iloc[0]))
 def test_last_valid_endpoint_is_labeled(self):
  f=pd.DataFrame({'date':['2020-01-02','2020-02-03','2020-03-02','2020-03-03'],'observed_session':[True]*4,'flagged':[False]*4,'discount_pct':[10.,10.,20.,np.nan],'preferred_raw_close':[90.,90.,80.,np.nan],'common_raw_close':[100.,100.,100.,np.nan]})
  m=monthly_grid(f,minimum=1,fraction=.5,last_complete='2020-03');q=quarterly_grid(m);self.assertEqual(str(q.quarter_end_last_valid_date.iloc[0].date()),'2020-03-02');self.assertEqual(q.quarter_end_staleness_proxy_rows.iloc[0],1)
 def test_calendar_horizon_not_compressed_and_strict(self):
  dates=pd.period_range('2000-01','2002-02',freq='M');m=pd.DataFrame({'qualified':True,'mean_q':np.arange(len(dates),dtype=float)},index=dates);m.loc['2001-01','qualified']=False;m.loc['2001-01','mean_q']=np.nan
  c=changes(m,[24]);row=c[c.end_month=='2002-01'].iloc[0];self.assertEqual(row.change_pp,24.);self.assertFalse(row.strict_complete);self.assertEqual(row.qualified_window_months,24)
 def test_state_gap_and_boundaries(self):
  m=pd.DataFrame({'mean_q':[9.,10.,19.,np.nan,20.,30.]},index=pd.period_range('2020-01',periods=6,freq='M'));r=state_runs(m);self.assertEqual(r.state.tolist(),['below_10','10_to_20','20_to_30','at_least_30']);self.assertEqual(r.months.tolist(),[1,2,1,1])
if __name__=='__main__':unittest.main()
