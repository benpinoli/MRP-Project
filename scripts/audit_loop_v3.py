"""Reconstruct rolling training dates, fits and aggregates independently for LH3.

Execute in Slurm under BYU_ORC_AGENTS.md; all outputs stay in ignored runs/.
"""
import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd

from audit_loop_v3_sources import read, known_date
from verify_loop_deliveries import digest

ROOT = Path(__file__).resolve().parents[1]


def verify_score(row, sub):
    assert len(sub) == row.forecast_n
    y = sub.actual_change_pp.to_numpy()
    mse = np.mean((y-sub.prediction_change_pp.to_numpy())**2)
    persistence = np.mean(y*y)
    mean_loss = np.mean((y-sub.training_mean_prediction.to_numpy())**2)
    assert np.isclose(np.sqrt(mse), row.rmse_pp, rtol=1e-10, atol=1e-9)
    assert np.isclose(1-mse/persistence, row.r2_vs_persistence, rtol=1e-9, atol=1e-8)
    assert np.isclose(1-mse/mean_loss, row.r2_vs_training_mean, rtol=1e-9, atol=1e-8)


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
    baseline, v2 = ROOT/cfg['baseline_run'], ROOT/cfg['stability_run']
    baseline_prov = json.loads((baseline/'provenance.json').read_text())
    models = {r['id']: r['columns'] for r in baseline_prov['config']['models']}
    panels = dict(tuple(pd.read_csv(baseline/'monthly.csv').groupby(['sample', 'variant'])))
    original = pd.read_csv(baseline/'forecasts.csv')
    failures = pd.read_csv(run/'failed_origins.csv')
    overall = pd.read_csv(run/'scores.csv')
    phases = pd.read_csv(run/'nonoverlap_phases.csv')
    periods = pd.read_csv(run/'calendar_periods.csv')
    group_cols = ['sample', 'variant', 'model', 'horizon_months']
    verified, aggregates, maximum_error = 0, 0, 0.
    cache = {}
    for keys, group_scores in overall.groupby(group_cols):
        sample, variant, model, horizon = keys
        prefix = f'{sample}_{variant}_{model}_{horizon}'
        frame = pd.read_csv(run/(prefix+'_forecasts.csv'))
        cache[keys] = frame
        expanding = pd.read_csv(v2/(prefix+'_forecasts.csv')).set_index(['origin_grid', 'method'])
        panel = panels[sample, variant].reset_index(drop=True)
        dates = pd.PeriodIndex(panel.month, freq='M')
        columns = models[model]
        x = panel[columns].to_numpy(float)
        q = panel.discount_pp.to_numpy(float)
        target = panel.discount_pp.shift(-int(horizon)).to_numpy()-q
        rolling = frame[frame.window == 'rolling120']
        for origin, predictions in rolling.groupby('origin_grid'):
            t = dates[int(origin)]
            train = ((dates >= t-cfg['rolling_training_origin_months']) & (dates < t) &
                     (dates+int(horizon) <= t) & np.isfinite(x).all(axis=1) & np.isfinite(target))
            n = int(train.sum())
            assert n >= max(cfg['minimum_training_observations'], cfg['observations_per_parameter']*(len(columns)+1))
            tx, ty = x[train], target[train]
            design = np.c_[np.ones(n), tx]
            ols = np.linalg.lstsq(design, ty, rcond=None)[0]
            mean, sd = tx.mean(axis=0), tx.std(axis=0)
            augmented = np.vstack([np.c_[np.ones(n), (tx-mean)/sd],
                np.c_[np.zeros(len(columns)), np.sqrt(n*cfg['ridge_penalty'])*np.eye(len(columns))]])
            ridge = np.linalg.lstsq(augmented, np.r_[ty, np.zeros(len(columns))], rcond=None)[0]
            expected = {'OLS': float(np.r_[1., x[int(origin)]]@ols),
                        'RIDGE': float(np.r_[1., (x[int(origin)]-mean)/sd]@ridge)}
            assert set(predictions.method) == {'OLS', 'RIDGE'} and len(predictions) == 2
            for row in predictions.itertuples():
                assert row.origin_month == str(t) and row.target_month == str(t+int(horizon))
                assert row.training_n == n
                assert row.first_training_grid == np.flatnonzero(train).min()
                assert row.last_training_grid == np.flatnonzero(train).max()
                assert row.latest_training_label_end_grid == np.flatnonzero(train).max()+int(horizon) <= origin
                assert np.isclose(row.actual_change_pp, target[int(origin)], rtol=0, atol=1e-10)
                assert np.isclose(row.training_mean_prediction, ty.mean(), rtol=0, atol=1e-10)
                err = abs(row.prediction_change_pp-expected[row.method])
                maximum_error = max(maximum_error, err)
                assert err < 1e-7
                verified += 1
        for row in frame[frame.window == 'expanding'].itertuples():
            old = expanding.loc[(row.origin_grid, row.method)]
            assert np.isclose(row.prediction_change_pp, old.prediction_change_pp, rtol=0, atol=1e-10)
        candidates = original[(original['sample'] == sample) & (original.variant == variant) &
            (original.model == model) & (original.horizon_months == horizon)]
        failed = failures[(failures['sample'] == sample) & (failures.variant == variant) &
            (failures.model == model) & (failures.horizon_months == horizon)]
        assert set(rolling.origin_month).isdisjoint(set(failed.origin_month))
        assert set(rolling.origin_month) | set(failed.origin_month) == set(candidates.origin_month)
        for row in group_scores.itertuples():
            sub = frame[(frame.window == row.window) & (frame.method == row.method)]
            verify_score(row, sub)
            aggregates += 1
            actual_phases = phases[(phases['sample'] == sample) & (phases.variant == variant) &
                (phases.model == model) & (phases.horizon_months == horizon) &
                (phases.window == row.window) & (phases.method == row.method)]
            assert set(actual_phases.phase) == set(sub.origin_grid % int(horizon))
            for phase_row in actual_phases.itertuples():
                selected = sub[sub.origin_grid % int(horizon) == phase_row.phase]
                assert np.all(np.diff(selected.origin_grid) >= int(horizon))
                verify_score(phase_row, selected)
                aggregates += 1
            actual_periods = periods[(periods['sample'] == sample) & (periods.variant == variant) &
                (periods.model == model) & (periods.horizon_months == horizon) &
                (periods.window == row.window) & (periods.method == row.method)]
            for period_row in actual_periods.itertuples():
                lo, hi = next((lo, hi) for name, lo, hi in cfg['calendar_periods'] if name == period_row.period)
                years = pd.PeriodIndex(sub.origin_month, freq='M').year
                verify_score(period_row, sub[(years >= lo) & (years <= hi)])
                aggregates += 1
    assert len(original) == verified//2+len(failures)
    incremental = pd.read_csv(run/'incremental.csv')
    for row in incremental.itertuples():
        a, b = [cache[row.sample, row.variant, model, row.horizon_months] for model in (row.simpler, row.larger)]
        matched = a[(a.window == row.window) & (a.method == row.method)].merge(
            b[(b.window == row.window) & (b.method == row.method)], on='origin_month', suffixes=('_a', '_b'))
        assert len(matched) == row.common_origins
        la = np.mean((matched.actual_change_pp_a-matched.prediction_change_pp_a)**2)
        lb = np.mean((matched.actual_change_pp_b-matched.prediction_change_pp_b)**2)
        assert np.isclose(1-lb/la, row.incremental_r2)
    admission = read(run/'source_review/evidence_admission.csv')
    assert len(admission) == 1375 and all(r['forecast_feature_admitted'] == 'False' for r in admission)
    tables = {}
    for row in admission:
        key = (row['source_snapshot'], row['source_table'])
        if key not in tables:
            tables[key] = {r['fact_id']: r for r in read(ROOT/'data/acquisition/2026-11-12'/key[0]/'prepared'/key[1])}
        original_fact = tables[key][row['fact_id']]
        assert all(row[field] == value for field, value in original_fact.items())
        assert (row['publication_date_known'] == 'True') == known_date(row['first_public_release_date'])
    for name, expected in prov['baseline_hashes'].items():
        assert digest(baseline/name) == expected
    for name, expected in prov['v2_hashes'].items():
        assert digest(v2/name) == expected
    for name, expected in prov['original_inputs'].items():
        assert digest(ROOT/name) == expected
    summary = {'status': 'passed', 'rolling_forecasts_reconstructed': verified,
        'max_prediction_error_pp': maximum_error, 'aggregate_score_rows_verified': aggregates,
        'incremental_rows_verified': len(incremental), 'all_candidate_origins_accounted_for': True,
        'fact_rows_preserved_without_feature_admission': len(admission),
        'baseline_and_v2_and_inputs_unchanged': True, 'independent_agent_review': False}
    (out/'AUDIT.json').write_text(json.dumps(summary, indent=2)+'\n')
    print(json.dumps(summary))


if __name__ == '__main__':
    main()
