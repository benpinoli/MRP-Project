"""LOOP-LH3 source integration and fixed calendar-memory check.

See BYU_ORC_AGENTS.md; run in Slurm and keep licensed rows in ignored runs/.
"""
import argparse
import json
import os
from pathlib import Path
import subprocess
import sys

import numpy as np
import pandas as pd

from audit_loop_v3_sources import audit_sources
from check_loop_stability import ridge_fit, save, score
from verify_loop_deliveries import digest

ROOT = Path(__file__).resolve().parents[1]


def training_mask(panel, y, columns, origin, horizon, window):
    return (panel[columns].notna().all(axis=1).to_numpy() & np.isfinite(y) &
            (panel.grid.to_numpy() < origin) & (panel.grid.to_numpy()+horizon <= origin) &
            (panel.grid.to_numpy() >= origin-window))


def checks():
    panel = pd.DataFrame({'grid': np.arange(300), 'x': np.arange(300, dtype=float)})
    for horizon, expected in [(24, 97), (60, 61), (120, 1)]:
        y = np.ones(300)
        mask = training_mask(panel, y, ['x'], 200, horizon, 120)
        assert mask.sum() == expected
        assert panel.grid[mask].min() == 80 and panel.grid[mask].max()+horizon == 200
    panel.loc[100, 'x'] = np.nan
    mask = training_mask(panel, np.ones(300), ['x'], 200, 60, 120)
    assert mask.sum() == 60 and not mask[100]
    panel.loc[201:, 'x'] = -1e12
    assert np.array_equal(mask, training_mask(panel, np.ones(300), ['x'], 200, 60, 120))
    return 5


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--config', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    out = args.output.resolve()
    assert out.is_relative_to(ROOT/'runs')
    out.mkdir(mode=0o700, parents=True, exist_ok=False)
    cfg = json.loads(args.config.read_text())
    save(out/'progress.json', {'status': 'started'})
    count_checks = checks()
    baseline, v2 = ROOT/cfg['baseline_run'], ROOT/cfg['stability_run']
    original = json.loads((baseline/'verification/AUDIT.json').read_text())['original_output_sha256']
    for name, expected in original.items():
        assert digest(baseline/name) == expected
    v2_hashes = json.loads((v2/'output_manifest.json').read_text())
    for name, expected in v2_hashes.items():
        assert digest(v2/name) == expected
    provenance = json.loads((baseline/'provenance.json').read_text())
    for name, expected in provenance['inputs'].items():
        assert digest(ROOT/name) == expected
    code = {}
    for name in ('run_loop_v3.py', 'audit_loop_v3_sources.py', 'check_loop_stability.py', 'verify_loop_deliveries.py'):
        path = ROOT/'scripts'/name
        (out/('executed_'+name)).write_bytes(path.read_bytes())
        code[name] = digest(path)
    save(out/'provenance.json', {'config': cfg, 'config_sha256': digest(args.config), 'code_sha256': code,
        'git_head': subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip(),
        'baseline_hashes': original, 'v2_hashes': v2_hashes, 'original_inputs': provenance['inputs'],
        'python': sys.version, 'numpy': np.__version__, 'pandas': pd.__version__,
        'slurm_job_id': os.environ.get('SLURM_JOB_ID'), 'validated_predictive_model': False})
    sources = out/'source_review'
    sources.mkdir(mode=0o700)
    source_audit = audit_sources(cfg, sources)
    save(out/'progress.json', {'status': 'source_audit_passed', 'source_audit': source_audit})
    panels = pd.read_csv(baseline/'monthly.csv')
    forecasts = pd.read_csv(baseline/'forecasts.csv')
    lookup = dict(tuple(panels.groupby(['sample', 'variant'])))
    models = {s['id']: s['columns'] for s in provenance['config']['models']}
    scores, phases, periods, failures, increments = [], [], [], [], []
    completed, total = 0, 0
    grouping = ['sample', 'variant', 'model', 'horizon_months']
    for keys, candidates in forecasts.groupby(grouping):
        sample, variant, model, horizon = keys
        base = dict(zip(grouping, keys))
        panel = lookup[sample, variant].reset_index(drop=True)
        columns = models[model]
        y = panel.discount_pp.shift(-int(horizon)).to_numpy()-panel.discount_pp.to_numpy()
        x = panel[columns].to_numpy(float)
        period = pd.PeriodIndex(panel.month, freq='M')
        assert period.equals(pd.period_range(period.min(), period.max(), freq='M'))
        assert np.array_equal(panel.grid, np.arange(len(panel)))
        prefix = f'{sample}_{variant}_{model}_{horizon}'
        expanding = pd.read_csv(v2/(prefix+'_forecasts.csv')).set_index(['origin_grid', 'method'])
        rows, coefficients = [], []
        for row in candidates.itertuples():
            origin = int(row.origin_grid)
            mask = training_mask(panel, y, columns, origin, int(horizon), cfg['rolling_training_origin_months'])
            n = int(mask.sum())
            minimum = max(cfg['minimum_training_observations'], cfg['observations_per_parameter']*(len(columns)+1))
            if n < minimum:
                failures.append({**base, 'origin_month': row.origin_month, 'training_n': n,
                                 'required': minimum, 'reason': 'rolling_matured_labels_below_minimum'})
                continue
            tx, ty = x[mask], y[mask]
            b = np.linalg.lstsq(np.c_[np.ones(n), tx], ty, rcond=None)[0]
            rb, _ = ridge_fit(tx, ty, cfg['ridge_penalty'])
            for method, beta in [('OLS', b), ('RIDGE', rb)]:
                common = {**base, 'method': method, 'origin_month': row.origin_month,
                    'target_month': row.target_month, 'origin_grid': origin, 'actual_change_pp': row.actual_change_pp}
                rows.append({**common, 'window': 'rolling120', 'training_n': n,
                    'first_training_grid': int(panel.grid[mask].min()), 'last_training_grid': int(panel.grid[mask].max()),
                    'latest_training_label_end_grid': int(panel.grid[mask].max())+int(horizon),
                    'training_mean_prediction': float(ty.mean()),
                    'prediction_change_pp': float(np.r_[1., x[origin]]@beta)})
                old = expanding.loc[(origin, method)]
                rows.append({**common, 'window': 'expanding', 'training_n': int(old.training_n),
                    'first_training_grid': None, 'last_training_grid': None,
                    'latest_training_label_end_grid': None,
                    'training_mean_prediction': float(old.training_mean_prediction),
                    'prediction_change_pp': float(old.prediction_change_pp)})
                for term, value in zip(['intercept']+columns, beta):
                    coefficients.append({**base, 'method': method, 'origin_month': row.origin_month,
                                         'term': term, 'coefficient': float(value), 'training_n': n})
        if not rows:
            continue
        frame = pd.DataFrame(rows)
        frame.to_csv(out/(prefix+'_forecasts.csv'), index=False)
        pd.DataFrame(coefficients).to_csv(out/(prefix+'_coefficients.csv'), index=False)
        for (window, method), group in frame.groupby(['window', 'method']):
            scores.append({**base, 'window': window, 'method': method, **score(group)})
            for phase in range(int(horizon)):
                sub = group[group.origin_grid % int(horizon) == phase]
                if len(sub):
                    phases.append({**base, 'window': window, 'method': method, 'phase': phase, **score(sub)})
            years = pd.PeriodIndex(group.origin_month, freq='M').year
            for label, lo, hi in cfg['calendar_periods']:
                sub = group[(years >= lo) & (years <= hi)]
                if len(sub):
                    periods.append({**base, 'window': window, 'method': method, 'period': label, **score(sub)})
        completed += 1
        total += len(frame)//4
        save(out/'progress.json', {'status': 'rolling_checks_running', 'completed_groups': completed,
                                   'successful_candidate_origins': total, 'last_group': list(keys)})
    # Nested feature comparisons within each training policy use common origins.
    groups = forecasts[['sample', 'variant', 'horizon_months']].drop_duplicates()
    for group in groups.itertuples(index=False):
        for simpler, larger in [('LH-LEVEL', 'LH-STATE'), ('LH-STATE', 'LH-ACTIVITY')]:
            paths = [out/f'{group.sample}_{group.variant}_{m}_{group.horizon_months}_forecasts.csv' for m in (simpler, larger)]
            if not all(p.exists() for p in paths):
                continue
            a, b = [pd.read_csv(p) for p in paths]
            for window in ('rolling120', 'expanding'):
                for method in ('OLS', 'RIDGE'):
                    matched = a[(a.window == window) & (a.method == method)].merge(
                        b[(b.window == window) & (b.method == method)], on='origin_month', suffixes=('_a', '_b'), validate='one_to_one')
                    if len(matched):
                        la = np.mean((matched.actual_change_pp_a-matched.prediction_change_pp_a)**2)
                        lb = np.mean((matched.actual_change_pp_b-matched.prediction_change_pp_b)**2)
                        increments.append({'sample': group.sample, 'variant': group.variant, 'horizon_months': group.horizon_months,
                            'window': window, 'method': method, 'simpler': simpler, 'larger': larger,
                            'common_origins': len(matched), 'incremental_r2': 1-lb/la if la else None})
    for name, rows in [('scores', scores), ('nonoverlap_phases', phases), ('calendar_periods', periods),
                       ('incremental', increments)]:
        pd.DataFrame(rows).to_csv(out/(name+'.csv'), index=False)
    pd.DataFrame(failures, columns=grouping+['origin_month', 'training_n', 'required', 'reason']).to_csv(out/'failed_origins.csv', index=False)
    (out/'baseline_model_status.csv').write_bytes((baseline/'model_status.csv').read_bytes())
    for name, expected in original.items():
        assert digest(baseline/name) == expected
    summary = {'status': 'completed', 'baseline_candidate_origins': len(forecasts),
        'matched_successful_origins': total, 'failed_rolling_origins': len(failures),
        'rolling_forecasts': total*2, 'completed_groups': completed, 'synthetic_checks': count_checks,
        'source_audit': source_audit, 'baseline_unchanged': True, 'validated_predictive_model': False}
    save(out/'summary.json', summary)
    save(out/'output_manifest.json', {str(p.relative_to(out)): digest(p) for p in out.rglob('*') if p.is_file() and p.name != 'progress.json'})
    save(out/'progress.json', summary)
    print(json.dumps(summary))


if __name__ == '__main__':
    main()
