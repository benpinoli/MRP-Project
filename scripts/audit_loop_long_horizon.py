"""Reconstruct forecast arithmetic and training chronology without the fit engine.

Run in Slurm under BYU_ORC_AGENTS.md. Save a separate audit and recoverable
per-class result checkpoint; never alter the original run tables.
"""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]


def digest(path):
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(1024*1024), b''):
            h.update(block)
    return h.hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--run', type=Path, required=True)
    parser.add_argument('--source-commit', required=True)
    args = parser.parse_args()
    run = args.run.resolve()
    if not run.is_relative_to(ROOT/'runs'):
        raise ValueError('Only private run directories')
    audit = run/'verification'
    audit.mkdir(exist_ok=False)
    provenance = json.loads((run/'provenance.json').read_text())
    cfg = provenance['config']
    original = subprocess.run(['git', 'show', args.source_commit+':scripts/run_loop_long_horizon.py'],
                              cwd=ROOT, capture_output=True, check=True).stdout
    assert hashlib.sha256(original).hexdigest() == provenance['code_sha256']
    (audit/'executed_source.py').write_bytes(original)
    for relative, expected in provenance['inputs'].items():
        assert digest(ROOT/relative) == expected, relative
    m = pd.read_csv(run/'monthly.csv')
    f = pd.read_csv(run/'forecasts.csv')
    models = {r['id']: r['columns'] for r in cfg['models']}
    lookup = {(s, v): x.set_index('month') for (s, v), x in m.groupby(['sample', 'variant'])}
    max_prediction_difference = 0.
    for (sample, variant, model, horizon), forecasts in f.groupby(['sample', 'variant', 'model', 'horizon_months']):
        monthly = lookup[sample, variant]
        period = pd.PeriodIndex(monthly.index, freq='M')
        columns = models[model]
        q = monthly.discount_pp.to_numpy(float)
        y = monthly.discount_pp.shift(-int(horizon))-monthly.discount_pp
        features = monthly[columns].to_numpy(float)
        for row in forecasts.itertuples():
            origin = int(row.origin_grid)
            assert str(period[origin]+int(horizon)) == row.target_month
            assert abs(q[origin+int(horizon)]-q[origin]-row.actual_change_pp) < 1e-10
            # This reconstructs the calendar-date rule directly, independently
            # of eligible_training(), grid-based masks and fit_ols().
            eligible = ((period < period[origin]) & (period+int(horizon) <= period[origin]) &
                        np.isfinite(features).all(axis=1) & y.notna().to_numpy())
            assert int(eligible.sum()) == row.training_n
            assert row.latest_training_label_end_grid <= origin
            x = np.column_stack([np.ones(eligible.sum()), features[eligible]])
            b = np.linalg.lstsq(x, y.to_numpy()[eligible], rcond=None)[0]
            prediction = float(np.r_[1., features[origin]]@b)
            difference = abs(prediction-row.prediction_change_pp)
            assert difference < 1e-7, (sample, model, origin, difference)
            max_prediction_difference = max(max_prediction_difference, difference)
    e = pd.read_csv(run/'evaluation.csv')
    for row in e.itertuples():
        z = f[(f['sample'] == row.sample) & (f.variant == row.variant) &
              (f.model == row.model) & (f.horizon_months == row.horizon_months)]
        mse = np.mean((z.actual_change_pp-z.prediction_change_pp)**2)
        baseline = np.mean(z.actual_change_pp**2)
        assert abs(1-mse/baseline-row.r2_vs_persistence) < 1e-10
    statuses = pd.read_csv(run/'model_status.csv')
    assert statuses.loc[statuses.horizon_months == 120, 'pseudo_oos_forecasts'].sum() == 0
    # Durable complete per-class copies are additive: original tiny completion
    # markers and the original aggregate tables are preserved unchanged.
    tables = {name: pd.read_csv(run/(name+'.csv')) for name in
        ('monthly', 'coefficients', 'forecasts', 'model_status', 'candidate_future_forecasts', 'coverage')}
    for sample in tables['coverage']['sample']:
        result = {name: json.loads(frame.loc[frame['sample'] == sample].to_json(orient='records'))
                  for name, frame in tables.items()}
        (audit/(sample+'_complete_checkpoint.json')).write_text(json.dumps(result)+'\n')
    hashes = {p.name: digest(p) for p in run.iterdir() if p.is_file()}
    (audit/'AUDIT.json').write_text(json.dumps({'verified_forecasts': len(f),
        'max_prediction_reconstruction_difference': max_prediction_difference,
        'evaluation_rows_verified': len(e), 'future_training_labels': 0,
        'source_commit': args.source_commit, 'original_output_sha256': hashes,
        'source_inputs_unchanged': True, 'complete_class_checkpoints': len(tables['coverage']),
        'independent_agent_review': False, 'method': 'Separate chronological mask and numpy least-squares reconstruction'}, indent=2)+'\n')
    print('Verified', len(f), 'forecast cases and', len(e), 'evaluation rows; no future-label leakage.')


if __name__ == '__main__':
    main()
