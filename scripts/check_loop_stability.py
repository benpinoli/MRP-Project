"""Frozen existing-sample LOOP diagnostics; execute in Slurm. See BYU_ORC_AGENTS.md."""
import argparse
import json
import os
from pathlib import Path
import subprocess
import sys
from datetime import datetime, timezone

import numpy as np
import pandas as pd

from verify_loop_deliveries import digest, verify_receipts

ROOT = Path(__file__).resolve().parents[1]


def save(path, value):
    tmp = path.with_suffix(path.suffix+'.pending')
    tmp.write_text(json.dumps(value, indent=2, allow_nan=False,
                              default=lambda x: x.item() if isinstance(x, np.generic) else str(x))+'\n')
    tmp.replace(path)


def ridge_fit(x, y, penalty):
    mean, scale = x.mean(axis=0), x.std(axis=0)
    if np.any(scale <= 0):
        raise ValueError('Constant predictor in baseline training')
    z = (x-mean)/scale
    centered = y-y.mean()
    slope = np.linalg.solve(z.T@z+len(y)*penalty*np.eye(x.shape[1]), z.T@centered)
    raw = slope/scale
    return np.r_[y.mean()-mean@raw, raw], slope


def synthetic_checks():
    x = np.array([[1., 9.], [2., 1.], [4., 5.], [7., 2.]])
    y = np.array([1., 4., 2., 8.])
    b, slopes = ridge_fit(x, y, 1.)
    z = (x-x.mean(axis=0))/x.std(axis=0)
    aug = np.vstack([np.column_stack([np.ones(len(x)), z]),
                     np.column_stack([np.zeros(2), np.sqrt(len(x))*np.eye(2)])])
    independent = np.linalg.lstsq(aug, np.r_[y, np.zeros(2)], rcond=None)[0]
    assert np.allclose(slopes, independent[1:])
    assert np.isclose(np.r_[1., x.mean(axis=0)]@b, y.mean())
    unpenalized, _ = ridge_fit(x, y, 0.)
    assert np.allclose(unpenalized, np.linalg.lstsq(np.c_[np.ones(4), x], y, rcond=None)[0])
    # Training fit invariant to units and to a separately held future outlier.
    rescaled, _ = ridge_fit(x*np.array([100., .01]), y, 1.)
    assert np.allclose(np.c_[np.ones(4), x]@b,
                       np.c_[np.ones(4), x*np.array([100., .01])]@rescaled)
    future = np.vstack([x, [1e9, -1e9]])
    assert np.allclose(ridge_fit(future[:4], y, 1.)[0], b)
    months = pd.period_range('2000-01', periods=100, freq='M')
    mask = (months < months[50]) & (months+24 <= months[50])
    assert mask.sum() == 27 and (months[mask]+24).max() == months[50]
    return 5


def score(frame):
    y = frame.actual_change_pp.to_numpy()
    loss = np.mean((y-frame.prediction_change_pp.to_numpy())**2)
    base = np.mean(y*y)
    historical = np.mean((y-frame.training_mean_prediction.to_numpy())**2)
    return {'forecast_n': len(frame), 'rmse_pp': float(np.sqrt(loss)),
            'r2_vs_persistence': float(1-loss/base) if base else None,
            'r2_vs_training_mean': float(1-loss/historical) if historical else None}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--config', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    out = args.output.resolve()
    assert out.is_relative_to(ROOT/'runs')
    out.mkdir(mode=0o700, parents=True, exist_ok=False)
    save(out/'progress.json', {'status': 'started', 'completed_groups': 0})
    cfg = json.loads(args.config.read_text())
    checks = synthetic_checks()
    receipts = verify_receipts(out)
    baseline = ROOT/cfg['baseline_run']
    audit = json.loads((baseline/'verification/AUDIT.json').read_text())
    original_hashes = audit['original_output_sha256']
    for name, expected in original_hashes.items():
        assert digest(baseline/name) == expected, name
    assert digest(baseline/'monthly.csv') == cfg['baseline_monthly_sha256']
    assert digest(baseline/'forecasts.csv') == cfg['baseline_forecasts_sha256']
    provenance = json.loads((baseline/'provenance.json').read_text())
    for name, expected in provenance['inputs'].items():
        assert digest(ROOT/name) == expected, name
    (out/'executed_source.py').write_bytes(Path(__file__).read_bytes())
    (out/'executed_receipt_verifier.py').write_bytes((ROOT/'scripts/verify_loop_deliveries.py').read_bytes())
    save(out/'provenance.json', {'config': cfg, 'config_sha256': digest(args.config),
         'code_sha256': digest(Path(__file__)), 'receipt_code_sha256': digest(ROOT/'scripts/verify_loop_deliveries.py'),
         'baseline_hashes': original_hashes, 'git_head': subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip(),
         'python': sys.version, 'numpy': np.__version__, 'pandas': pd.__version__,
         'job_id': os.environ.get('SLURM_JOB_ID'), 'validated_predictive_model': False})
    monthly = pd.read_csv(baseline/'monthly.csv')
    forecasts = pd.read_csv(baseline/'forecasts.csv')
    models = {s['id']: s['columns'] for s in provenance['config']['models']}
    lookup = dict(tuple(monthly.groupby(['sample', 'variant'])))
    all_scores, all_phases, all_periods, drift_summary, increments = [], [], [], [], []
    max_error, ridge_error, total = 0., 0., 0
    group_cols = ['sample', 'variant', 'model', 'horizon_months']
    for keys, f in forecasts.groupby(group_cols):
        base = dict(zip(group_cols, keys))
        sample, variant, model, horizon = keys
        panel = lookup[sample, variant].reset_index(drop=True)
        period = pd.PeriodIndex(panel.month, freq='M')
        assert period.equals(pd.period_range(period.min(), period.max(), freq='M'))
        assert np.array_equal(panel.grid.to_numpy(), np.arange(len(panel)))
        x = panel[models[model]].to_numpy(float)
        q = panel.discount_pp.to_numpy(float)
        y = panel.discount_pp.shift(-int(horizon)).to_numpy()-q
        records, drift = [], []
        for row in f.itertuples():
            origin = int(row.origin_grid)
            eligible = ((period < period[origin]) & (period+int(horizon) <= period[origin]) &
                        np.isfinite(x).all(axis=1) & np.isfinite(y))
            n = int(eligible.sum())
            assert n == row.training_n and n >= max(provenance['config']['minimum_training_observations'],
                       provenance['config']['observations_per_parameter']*(x.shape[1]+1))
            assert row.target_month == str(period[origin]+int(horizon))
            assert np.isclose(y[origin], row.actual_change_pp, atol=1e-10, rtol=0)
            train_x, train_y = x[eligible], y[eligible]
            design = np.column_stack([np.ones(n), train_x])
            b = np.linalg.lstsq(design, train_y, rcond=None)[0]
            raw, standardized = ridge_fit(train_x, train_y, cfg['ridge_penalty'])
            value = np.r_[1., x[origin]]
            delta = abs(float(value@b)-row.prediction_change_pp)
            max_error = max(max_error, delta)
            assert delta < 1e-7
            # Independent augmented-design ridge reconstruction, intercept unpenalized.
            z = (train_x-train_x.mean(axis=0))/train_x.std(axis=0)
            augmented = np.vstack([np.c_[np.ones(n), z], np.c_[np.zeros(x.shape[1]),
                                   np.sqrt(n*cfg['ridge_penalty'])*np.eye(x.shape[1])]])
            check = np.linalg.lstsq(augmented, np.r_[train_y, np.zeros(x.shape[1])], rcond=None)[0]
            prediction = float(value@raw)
            err = abs(prediction-float(np.r_[1., (x[origin]-train_x.mean(axis=0))/train_x.std(axis=0)]@check))
            ridge_error = max(ridge_error, err)
            assert err < 1e-7
            common = {**base, 'origin_month': row.origin_month, 'target_month': row.target_month,
                      'origin_grid': origin, 'training_n': n, 'last_training_origin': str(period[eligible].max()),
                      'latest_training_label_end': str((period[eligible]+int(horizon)).max()),
                      'actual_change_pp': row.actual_change_pp, 'training_mean_prediction': row.training_mean_prediction}
            assert np.isclose(train_y.mean(), row.training_mean_prediction, atol=1e-10, rtol=0)
            for method, coefficients, std in [('OLS', b, b[1:]*train_x.std(axis=0)),
                                               ('RIDGE', raw, standardized)]:
                records.append({**common, 'method': method, 'prediction_change_pp': float(value@coefficients)})
                for term, coef, standardized_coef in zip(['intercept']+models[model], coefficients, [np.nan]+list(std)):
                    drift.append({**base, 'method': method, 'origin_month': row.origin_month,
                                  'term': term, 'coefficient': coef, 'training_sd_coefficient': standardized_coef,
                                  'training_n': n})
        predicted, coefficients = pd.DataFrame(records), pd.DataFrame(drift)
        prefix = f'{sample}_{variant}_{model}_{horizon}'
        predicted.to_csv(out/(prefix+'_forecasts.csv'), index=False)
        coefficients.to_csv(out/(prefix+'_coefficients.csv'), index=False)
        for method, group in predicted.groupby('method'):
            all_scores.append({**base, 'method': method, **score(group)})
            for phase in range(int(horizon)):
                sub = group[group.origin_grid % int(horizon) == phase]
                if len(sub):
                    assert np.all(np.diff(sub.origin_grid.to_numpy()) >= int(horizon))
                    all_phases.append({**base, 'method': method, 'phase': phase, **score(sub)})
            years = pd.PeriodIndex(group.origin_month, freq='M').year
            for name, lo, hi in cfg['calendar_periods']:
                sub = group[(years >= lo) & (years <= hi)]
                if len(sub):
                    all_periods.append({**base, 'method': method, 'period': name, **score(sub)})
        for (method, term), group in coefficients.groupby(['method', 'term']):
            c = group.coefficient.to_numpy()
            drift_summary.append({**base, 'method': method, 'term': term, 'origin_n': len(c),
                'first_coefficient': c[0], 'last_coefficient': c[-1], 'minimum': c.min(), 'maximum': c.max(),
                'sign_transitions': int(np.sum(np.sign(c[1:]) != np.sign(c[:-1])))})
        total += len(f)
        save(out/'progress.json', {'status': 'running', 'verified_baseline_forecasts': total,
                                   'last_completed_group': list(keys)})
    # Compare each nested specification only on common origins under each method.
    for (sample, variant, horizon), f in forecasts.groupby(['sample', 'variant', 'horizon_months']):
        for method in ('OLS', 'RIDGE'):
            for simpler, larger in [('LH-LEVEL', 'LH-STATE'), ('LH-STATE', 'LH-ACTIVITY')]:
                prefix = f'{sample}_{variant}_'
                left = out/f'{prefix}{simpler}_{horizon}_forecasts.csv'
                right = out/f'{prefix}{larger}_{horizon}_forecasts.csv'
                if not (left.exists() and right.exists()):
                    continue
                a, b = pd.read_csv(left), pd.read_csv(right)
                matched = a[a.method == method].merge(b[b.method == method], on='origin_month', suffixes=('_a', '_b'), validate='one_to_one')
                if len(matched):
                    assert np.allclose(matched.actual_change_pp_a, matched.actual_change_pp_b)
                    loss_a = np.mean((matched.actual_change_pp_a-matched.prediction_change_pp_a)**2)
                    loss_b = np.mean((matched.actual_change_pp_b-matched.prediction_change_pp_b)**2)
                    increments.append({'sample': sample, 'variant': variant, 'horizon_months': horizon,
                        'method': method, 'simpler': simpler, 'larger': larger, 'common_origins': len(matched),
                        'incremental_r2': 1-loss_b/loss_a if loss_a else None})
    for name, rows in [('scores', all_scores), ('nonoverlap_phases', all_phases), ('calendar_periods', all_periods),
                        ('coefficient_drift', drift_summary), ('incremental', increments)]:
        pd.DataFrame(rows).to_csv(out/(name+'.csv'), index=False)
    # Record all blocked LH1 fits, including the lack of ten-year forecasts.
    (out/'baseline_model_status.csv').write_bytes((baseline/'model_status.csv').read_bytes())
    for name, expected in original_hashes.items():
        assert digest(baseline/name) == expected
    summary = {'status': 'completed', 'baseline_forecasts_verified': total, 'ridge_forecasts': total,
        'max_ols_reconstruction_error': max_error, 'max_ridge_reconstruction_error': ridge_error,
        'synthetic_checks': checks, 'baseline_unchanged': True, 'new_intervals_released': 0,
        'deliveries': [{'snapshot': r['snapshot'], 'status': r['status']} for r in receipts],
        'completed_utc': datetime.now(timezone.utc).isoformat(), 'validated_predictive_model': False}
    save(out/'summary.json', summary)
    save(out/'output_manifest.json', {p.name: digest(p) for p in out.iterdir() if p.is_file() and p.name != 'progress.json'})
    save(out/'progress.json', summary)
    print(json.dumps(summary))


if __name__ == '__main__':
    main()
