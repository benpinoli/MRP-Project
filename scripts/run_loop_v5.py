"""One positive conditional mean versus three anchors. See BYU_ORC_AGENTS.md."""
import argparse
import json
import os
from pathlib import Path
import subprocess

import numpy as np
import pandas as pd

from check_loop_stability import save
from positive_ratio_mean import fit_ratio_mean, predict_ratio
from verify_loop_deliveries import digest

ROOT = Path(__file__).resolve().parents[1]


def scores(frame):
    actual = frame.actual_change_pp.to_numpy(float)
    error = actual-frame.prediction_change_pp.to_numpy(float)
    mse = float(np.mean(error**2))
    result = {'forecast_n': len(frame), 'mse_pp2': mse, 'rmse_pp': float(np.sqrt(mse)),
              'mae_pp': float(np.mean(abs(error)))}
    for label, column in [('persistence', 'zero_prediction'), ('mean_change', 'mean_change_prediction'),
                          ('terminal_mean', 'terminal_mean_prediction')]:
        loss = float(np.mean((actual-frame[column].to_numpy(float))**2))
        result[label+'_mse_pp2'] = loss
        result['r2_vs_'+label] = 1-mse/loss if loss > 0 else None
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--config', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    cfg = json.loads(args.config.read_text())
    out = args.output.resolve()
    assert out.is_relative_to(ROOT/'runs')
    out.mkdir(mode=0o700, parents=True, exist_ok=False)
    save(out/'progress.json', {'status': 'started'})
    baseline, ridge = ROOT/cfg['baseline_run'], ROOT/cfg['ridge_run']
    protected = {str(baseline/name): expected for name, expected in
                 json.loads((baseline/'verification/AUDIT.json').read_text())['original_output_sha256'].items()}
    protected.update({str(ridge/name): expected for name, expected in json.loads((ridge/'output_manifest.json').read_text()).items()})
    original_prov = json.loads((baseline/'provenance.json').read_text())
    protected.update({str(ROOT/name): expected for name, expected in original_prov['inputs'].items()})
    for name, expected in protected.items():
        assert digest(Path(name)) == expected
    for name in ('run_loop_v5.py', 'positive_ratio_mean.py'):
        (out/('executed_'+name)).write_bytes((ROOT/'scripts'/name).read_bytes())
    (out/'frozen_config.json').write_bytes(args.config.read_bytes())
    save(out/'provenance.json', {'config': cfg, 'config_sha256': digest(args.config),
        'executed_source_sha256': digest(Path(__file__)),
        'mean_fit_source_sha256': digest(ROOT/'scripts/positive_ratio_mean.py'),
        'protected_inputs': protected, 'job_id': os.environ.get('SLURM_JOB_ID'),
        'git_head': subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip(),
        'numpy': np.__version__, 'pandas': pd.__version__, 'validated_predictive_model': False})
    monthly = pd.read_csv(baseline/'monthly.csv')
    lookup = dict(tuple(monthly.groupby(['sample', 'variant'])))
    requested = pd.read_csv(baseline/'forecasts.csv')
    requested = requested[requested.model == 'LH-LEVEL']
    requested.to_csv(out/'requested_original_forecasts.csv', index=False)
    aggregate, phases, periods, failures = [], [], [], []
    successes, support_rounding = 0, 0
    for keys, original in requested.groupby(['sample', 'variant', 'horizon_months']):
        sample, variant, horizon = keys
        base = {'sample': sample, 'variant': variant, 'horizon_months': int(horizon)}
        panel = lookup[sample, variant].reset_index(drop=True)
        dates = pd.PeriodIndex(panel.month, freq='M')
        assert dates.equals(pd.period_range(dates.min(), dates.max(), freq='M'))
        assert np.array_equal(panel.grid.to_numpy(), np.arange(len(panel)))
        q = panel.discount_pp.to_numpy(float)
        ratios = 1-q/100
        target_ratio = pd.Series(ratios).shift(-int(horizon)).to_numpy()
        valid = np.isfinite(ratios) & np.isfinite(target_ratio)
        assert (ratios[np.isfinite(ratios)] > 0).all()
        grid = np.arange(len(panel))
        ridge_frame = pd.read_csv(ridge/f'{sample}_{variant}_LH-LEVEL_{horizon}_forecasts.csv')
        ridge_frame = ridge_frame[ridge_frame.method == 'RIDGE'].set_index('origin_grid')
        rows, fits = [], []
        for row in original.itertuples():
            origin = int(row.origin_grid)
            mask = valid & (grid < origin) & (grid+int(horizon) <= origin)
            n = int(mask.sum())
            assert n == row.training_n and n >= max(cfg['minimum_training_observations'], cfg['observations_per_parameter']*2)
            terminal_q = 100*(1-target_ratio[mask])
            mean_change = float(np.mean(terminal_q-q[mask]))
            mean_terminal = float(terminal_q.mean()-q[origin])
            assert np.isclose(mean_change, row.training_mean_prediction, rtol=0, atol=1e-10)
            try:
                fit = fit_ratio_mean(ratios[mask], target_ratio[mask])
                prediction_ratio = predict_ratio(fit, ratios[origin])
                prediction_q = 100*(1-prediction_ratio)
                prediction_change = 100*(ratios[origin]-prediction_ratio)
                assert np.isclose(prediction_q-q[origin], prediction_change, rtol=0, atol=1e-10)
            except (ValueError, FloatingPointError) as error:
                failures.append({**base, 'origin_grid': origin, 'origin_month': row.origin_month,
                                 'training_n': n, 'reason': str(error)})
                continue
            if prediction_q >= 100:
                support_rounding += 1
            common = {**base, 'origin_grid': origin, 'origin_month': row.origin_month,
                'target_month': row.target_month, 'training_n': n,
                'latest_training_label_end_grid': int(grid[mask].max())+int(horizon),
                'actual_change_pp': row.actual_change_pp, 'origin_discount_pp': q[origin],
                'zero_prediction': 0., 'mean_change_prediction': mean_change,
                'terminal_mean_prediction': mean_terminal}
            for method, prediction in [('PPML-MEAN', prediction_change), ('OLS', row.prediction_change_pp),
                                        ('RIDGE', float(ridge_frame.loc[origin].prediction_change_pp))]:
                rows.append({**common, 'method': method, 'prediction_change_pp': float(prediction)})
            fits.append({**base, 'origin_grid': origin, 'origin_month': row.origin_month,
                'training_n': n, 'predicted_terminal_ratio': prediction_ratio,
                'predicted_terminal_discount_pp': prediction_q, **fit})
            successes += 1
        prefix = f'{sample}_{variant}_{horizon}'
        frame = pd.DataFrame(rows)
        frame.to_csv(out/(prefix+'_forecasts.csv'), index=False)
        pd.DataFrame(fits).to_csv(out/(prefix+'_fits.csv'), index=False)
        if len(frame):
            for method, group in frame.groupby('method'):
                aggregate.append({**base, 'method': method, 'requested_origins': len(original),
                    'failed_origins': len(original)-len(group), **scores(group)})
                for phase in range(int(horizon)):
                    sub = group[group.origin_grid % int(horizon) == phase]
                    if len(sub):
                        phases.append({**base, 'method': method, 'phase': phase, **scores(sub)})
                years = pd.PeriodIndex(group.origin_month, freq='M').year
                for label, lo, hi in cfg['calendar_periods']:
                    sub = group[(years >= lo) & (years <= hi)]
                    if len(sub):
                        periods.append({**base, 'method': method, 'period': label, **scores(sub)})
        save(out/'progress.json', {'status': 'running', 'last_group': list(keys),
            'successful_origins': successes, 'failed_origins': len(failures)})
    pd.DataFrame(aggregate).to_csv(out/'scores.csv', index=False)
    pd.DataFrame(phases).to_csv(out/'nonoverlap_phases.csv', index=False)
    pd.DataFrame(periods).to_csv(out/'calendar_periods.csv', index=False)
    pd.DataFrame(failures, columns=['sample', 'variant', 'horizon_months', 'origin_grid', 'origin_month', 'training_n', 'reason']).to_csv(out/'failed_origins.csv', index=False)
    statuses = pd.read_csv(baseline/'model_status.csv')
    statuses = statuses[statuses.model == 'LH-LEVEL'].copy()
    statuses['v5_scope'] = 'Original eligible origins only; blocked cases are not losses'
    statuses.to_csv(out/'original_model_status.csv', index=False)
    for name, expected in protected.items():
        assert digest(Path(name)) == expected
    summary = {'status': 'completed', 'requested_origins': len(requested), 'successful_origins': successes,
        'failed_origins': len(failures), 'score_rows': len(aggregate), 'phase_rows': len(phases),
        'nonpositive_or_nonfinite_forecast_ratios': 0, 'terminal_q_rounded_to_100': support_rounding,
        'baseline_and_ridge_and_inputs_unchanged': True, 'new_intervals': 0,
        'new_structural_features': 0, 'validated_predictive_model': False}
    save(out/'summary.json', summary)
    save(out/'output_manifest.json', {p.name: digest(p) for p in out.iterdir() if p.is_file() and p.name != 'progress.json'})
    save(out/'progress.json', summary)
    print((out/'summary.json').read_text())


if __name__ == '__main__':
    main()
