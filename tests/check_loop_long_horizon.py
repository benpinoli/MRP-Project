"""Calendar endpoints, no-future training and monthly ratio aggregation."""
import importlib.util
from pathlib import Path
import unittest
import json
import tempfile

import numpy as np
import pandas as pd

spec = importlib.util.spec_from_file_location('loop_lh', Path(__file__).resolve().parents[1]/'scripts/run_loop_long_horizon.py')
lh = importlib.util.module_from_spec(spec)
spec.loader.exec_module(lh)


class HorizonChecks(unittest.TestCase):
    def test_missing_month_does_not_compress_target(self):
        x = pd.DataFrame({'discount_pp': [10., np.nan, 30., 40.]},
                         index=pd.period_range('2020-01', periods=4, freq='M'))
        y = lh.labels(x, 2)
        self.assertEqual(y.iloc[0], 20.)
        self.assertTrue(np.isnan(y.iloc[1]))

    def test_training_uses_only_matured_labels(self):
        x = pd.DataFrame({'discount_pp': np.arange(30.), 'grid': np.arange(30)})
        y = lh.labels(x, 12)
        mask = lh.eligible_training(x, y, ['discount_pp'], 20, 12)
        self.assertEqual(x.loc[mask, 'grid'].max(), 8)
        self.assertFalse(mask.iloc[9])
        altered = x.copy()
        altered.loc[21:, 'discount_pp'] = 100000.
        altered_y = lh.labels(altered, 12)
        np.testing.assert_array_equal(y[mask], altered_y[mask])

    def test_monthly_averages_ratios_without_filling_empty_month(self):
        daily = pd.DataFrame({'date': pd.to_datetime(['2020-01-02', '2020-01-03', '2020-03-02']),
                              'discount_pp': [10., 30., 50.], 'activity': [0., 1., 2.]})
        denominator = pd.DataFrame({'date': pd.to_datetime(['2020-01-02', '2020-01-03', '2020-02-03', '2020-03-02'])})
        m = lh.monthly_panel(daily, denominator, '2020-03', .5, 1)
        self.assertEqual(m.iloc[0].discount_pp, 20.)
        self.assertTrue(np.isnan(m.iloc[1].discount_pp))
        self.assertEqual(len(m), 3)

    def test_pragmatic_and_strict_coverage_are_explicit(self):
        denominator = pd.DataFrame({'date': pd.date_range('2020-01-01', periods=10, freq='B')})
        daily = denominator.iloc[:6].assign(discount_pp=10., activity=0.)
        self.assertTrue(lh.monthly_panel(daily, denominator, '2020-01', .5, 5).iloc[0].qualified)
        self.assertFalse(lh.monthly_panel(daily, denominator, '2020-01', .8, 5).iloc[0].qualified)

    def test_durable_checkpoint_preserves_results_and_replaces_atomically(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp)/'checkpoint.json'
            record = {'sample': 'synthetic', 'variants': {'main': {'forecasts': [{'prediction': 1.25}]}}}
            lh.save_json(path, record)
            self.assertEqual(json.loads(path.read_text()), record)
            self.assertFalse(Path(str(path)+'.pending').exists())
            record['status'] = 'completed'
            lh.save_json(path, record)
            self.assertEqual(json.loads(path.read_text())['status'], 'completed')


if __name__ == '__main__':
    unittest.main()
