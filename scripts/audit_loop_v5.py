"""Independent two-parameter quasi-mean reconstruction. See BYU_ORC_AGENTS.md."""
import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd

from verify_loop_deliveries import digest

ROOT = Path(__file__).resolve().parents[1]


def reference_mean(x, y, current):
    # Full two-dimensional Newton fit, independent of profiled slope bisection.
    lx = np.log(x)
    z = (lx-lx.mean())/lx.std()
    design = np.c_[np.ones(len(x)), z]
    ymean = y.mean()
    scaled = y/ymean
    theta = np.zeros(2)
    for _ in range(100):
        mu = np.exp(design@theta)
        gradient = design.T@(mu-scaled)/len(x)
        if np.max(abs(gradient)) < 3e-13:
            break
        hessian = design.T@(design*mu[:, None])/len(x)
        direction = np.linalg.solve(hessian, gradient)
        step = 1.
        for _ in range(60):
            delta = -step*(design@direction)
            with np.errstate(over='ignore', invalid='ignore'):
                difference = np.mean(mu*np.expm1(delta)-scaled*delta)
            if np.isfinite(difference) and difference <= -1e-4*step*float(gradient@direction):
                theta -= step*direction
                break
            step /= 2
        else:
            raise AssertionError('Independent Newton line search failed')
    assert np.max(abs(design.T@(np.exp(design@theta)-scaled)/len(x))) < 1e-10
    return float(ymean*np.exp(np.r_[1., (np.log(current)-lx.mean())/lx.std()]@theta))


def verify_score(row, frame):
    assert len(frame) == row.forecast_n
    actual = frame.actual_change_pp.to_numpy()
    error = actual-frame.prediction_change_pp.to_numpy()
    loss = np.mean(error**2)
    assert np.isclose(row.mse_pp2, loss, rtol=1e-10, atol=1e-10)
    assert np.isclose(row.rmse_pp, np.sqrt(loss), rtol=1e-10, atol=1e-10)
    assert np.isclose(row.mae_pp, np.mean(abs(error)), rtol=1e-10, atol=1e-10)
    for label, column in [('persistence', 'zero_prediction'), ('mean_change', 'mean_change_prediction'),
                          ('terminal_mean', 'terminal_mean_prediction')]:
        benchmark = np.mean((actual-frame[column].to_numpy())**2)
        assert np.isclose(getattr(row, label+'_mse_pp2'), benchmark, rtol=1e-10, atol=1e-10)
        assert np.isclose(getattr(row, 'r2_vs_'+label), 1-loss/benchmark, rtol=1e-9, atol=1e-9)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--run', type=Path, required=True)
    args = parser.parse_args()
    run = args.run.resolve()
    assert run.is_relative_to(ROOT/'runs')
    out = run/'verification'
    out.mkdir(mode=0o700, exist_ok=False)
    (out/'executed_source.py').write_bytes(Path(__file__).read_bytes())
    for name, expected in json.loads((run/'output_manifest.json').read_text()).items():
        assert digest(run/name) == expected
    prov = json.loads((run/'provenance.json').read_text())
    cfg = prov['config']
    baseline, ridge = ROOT/cfg['baseline_run'], ROOT/cfg['ridge_run']
    panels = dict(tuple(pd.read_csv(baseline/'monthly.csv').groupby(['sample', 'variant'])))
    requested = pd.read_csv(run/'requested_original_forecasts.csv')
    overall = pd.read_csv(run/'scores.csv')
    phases = pd.read_csv(run/'nonoverlap_phases.csv')
    periods = pd.read_csv(run/'calendar_periods.csv')
    failed = pd.read_csv(run/'failed_origins.csv')
    maximum, verified, score_rows = 0., 0, 0
    for keys, scores in overall.groupby(['sample', 'variant', 'horizon_months']):
        sample, variant, horizon = keys
        panel = panels[sample, variant].reset_index(drop=True)
        dates = pd.PeriodIndex(panel.month, freq='M')
        q = panel.discount_pp.to_numpy(float)
        ratio = 1-q/100
        target_q = panel.discount_pp.shift(-int(horizon)).to_numpy()
        original = requested[(requested['sample'] == sample) & (requested.variant == variant) & (requested.horizon_months == horizon)]
        frame = pd.read_csv(run/f'{sample}_{variant}_{horizon}_forecasts.csv')
        ridge_values = pd.read_csv(ridge/f'{sample}_{variant}_LH-LEVEL_{horizon}_forecasts.csv')
        ridge_values = ridge_values[ridge_values.method == 'RIDGE'].set_index('origin_grid')
        for method in ('OLS', 'RIDGE', 'PPML-MEAN'):
            assert list(frame[frame.method == method].origin_month) == list(original.origin_month)
        old = original.set_index('origin_grid')
        for origin, predictions in frame.groupby('origin_grid'):
            origin = int(origin)
            mask = ((dates < dates[origin]) & (dates+int(horizon) <= dates[origin]) &
                    np.isfinite(q) & np.isfinite(target_q))
            n = int(mask.sum())
            assert n == int(predictions.training_n.iloc[0])
            prediction = reference_mean(ratio[mask], 1-target_q[mask]/100, ratio[origin])
            assert prediction > 0 and np.isfinite(prediction)
            expected = 100*(ratio[origin]-prediction)
            actual_row = predictions[predictions.method == 'PPML-MEAN'].iloc[0]
            error = abs(expected-actual_row.prediction_change_pp)
            maximum = max(maximum, error)
            assert error < 1e-7
            for row in predictions.itertuples():
                assert row.target_month == str(dates[origin]+int(horizon))
                assert row.latest_training_label_end_grid <= origin
                assert np.isclose(row.actual_change_pp, target_q[origin]-q[origin], rtol=0, atol=1e-10)
                assert np.isclose(row.mean_change_prediction, (target_q[mask]-q[mask]).mean(), rtol=0, atol=1e-10)
                assert np.isclose(row.terminal_mean_prediction, target_q[mask].mean()-q[origin], rtol=0, atol=1e-10)
                if row.method == 'OLS':
                    assert np.isclose(row.prediction_change_pp, old.loc[origin].prediction_change_pp, rtol=0, atol=1e-10)
                elif row.method == 'RIDGE':
                    assert np.isclose(row.prediction_change_pp, ridge_values.loc[origin].prediction_change_pp, rtol=0, atol=1e-10)
            verified += 1
        for row in scores.itertuples():
            group = frame[frame.method == row.method]
            verify_score(row, group); score_rows += 1
            sub_phases = phases[(phases['sample'] == sample) & (phases.variant == variant) &
                (phases.horizon_months == horizon) & (phases.method == row.method)]
            assert set(sub_phases.phase) == set(group.origin_grid % int(horizon))
            for r in sub_phases.itertuples():
                sub = group[group.origin_grid % int(horizon) == r.phase]
                assert np.all(np.diff(sub.origin_grid) >= int(horizon))
                verify_score(r, sub); score_rows += 1
            sub_periods = periods[(periods['sample'] == sample) & (periods.variant == variant) &
                (periods.horizon_months == horizon) & (periods.method == row.method)]
            years = pd.PeriodIndex(group.origin_month, freq='M').year
            for r in sub_periods.itertuples():
                lo, hi = next((lo, hi) for label, lo, hi in cfg['calendar_periods'] if label == r.period)
                verify_score(r, group[(years >= lo) & (years <= hi)]); score_rows += 1
    assert verified == len(requested) and len(failed) == 0
    for name, expected in prov['protected_inputs'].items():
        assert digest(Path(name)) == expected
    result = {'status': 'passed', 'quasi_mean_forecasts_reconstructed': verified,
        'maximum_prediction_difference_pp': maximum, 'score_phase_period_rows_verified': score_rows,
        'three_benchmarks_same_matured_rows_verified': True, 'positive_ratio_support_verified': True,
        'all_original_origins_accounted_for': True, 'baseline_and_ridge_and_inputs_unchanged': True,
        'independent_agent_review': False, 'method': 'Full two-parameter Newton mean scores versus profiled bisection'}
    (out/'AUDIT.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result))


if __name__ == '__main__':
    main()
