import os,unittest
os.environ.setdefault('SAMSUNG_REPO',os.getcwd())
import numpy as np
import pandas as pd
from samsung_research.prediction_candidate_archive import eligible
class CandidateChecks(unittest.TestCase):
    def test_purge_and_preserved_gaps(self):
        q=pd.Series(np.arange(100,dtype=float));q.iloc[40]=np.nan
        y,d,m=eligible(q,90,5);ix=np.flatnonzero(m)
        self.assertLess(ix[-1]+5,90);self.assertFalse(m[35]);self.assertFalse(m[40]);self.assertFalse(m[41]);self.assertTrue(m[42]);self.assertEqual(y.iloc[42],5)
        q.iloc[90:]=10000;y2,d2,m2=eligible(q,90,5);np.testing.assert_array_equal(m,m2);np.testing.assert_allclose(y[m],y2[m])
if __name__=='__main__':unittest.main()
