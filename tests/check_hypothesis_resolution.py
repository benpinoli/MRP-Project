import unittest

import numpy as np
import pandas as pd

from samsung_research.hypothesis_resolution import hc1_ols, partial_permutation_p


class HypothesisResolutionChecks(unittest.TestCase):
    def test_hc1_ols_recovers_line(self):
        x = np.arange(30.0)
        y = 2 + 3 * x
        b, se, p, r2 = hc1_ols(y, np.column_stack([np.ones(len(x)), x]))
        np.testing.assert_allclose(b, [2, 3], atol=1e-12)
        self.assertAlmostEqual(r2, 1.0)

    def test_partial_permutation_detects_target_not_nuisance_only(self):
        rng = np.random.default_rng(4)
        nuisance = rng.normal(size=80)
        target = rng.normal(size=80)
        y = 2 * nuisance + target + rng.normal(scale=.1, size=80)
        p = partial_permutation_p(y, target, nuisance[:, None], 999, np.random.default_rng(5))
        self.assertLess(p, .01)


if __name__ == "__main__":
    unittest.main()
