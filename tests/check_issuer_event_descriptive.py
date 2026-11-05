import os, unittest
os.environ.setdefault('SAMSUNG_REPO',os.getcwd())
import numpy as np
import pandas as pd
from samsung_research.issuer_event_descriptive import event_windows,cash_discount_delta
class EventChecks(unittest.TestCase):
 def test_next_session_and_missing_interval(self):
  g=pd.DataFrame({'date':['2025-01-03','2025-01-06','2025-01-07','2025-01-08'],'discount_pct':[20.,21.,np.nan,23.],'flagged':[False]*4})
  r=event_windows(g,{'id':'x','kind':'x','cluster':'x','publication_date':'2025-01-04'},[1,2]);self.assertEqual(r[0]['status'],'base_missing');self.assertEqual(r[2]['base_date'],'2025-01-06');self.assertEqual(r[2]['status'],'invalid_endpoint');self.assertEqual(r[3]['change_pp'],2.);self.assertFalse(r[3]['strict_interval'])
 def test_cash_identity(self):
  c,p,dc,dp=10000.,8000.,363.,364.;expected=100*(1-(p-dp)/(c-dc))-100*(1-p/c)
  self.assertAlmostEqual(cash_discount_delta(c,p,dc,dp),expected);self.assertGreater(cash_discount_delta(c,p,300.,300.),0)
if __name__=='__main__':unittest.main()
