"""Verify LH4 benchmark, bound and unit diagnostics without changing prior results.

Run in Slurm; follow BYU_ORC_AGENTS.md. This does not refit a predictive model.
"""
import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd

from audit_loop_v3_sources import read, known_date
from verify_loop_deliveries import digest

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--run', type=Path, required=True)
    parser.add_argument('--verification-name', default='verification')
    args = parser.parse_args()
    run = args.run.resolve()
    assert run.is_relative_to(ROOT/'runs')
    assert Path(args.verification_name).name == args.verification_name
    out = run/args.verification_name
    out.mkdir(mode=0o700, exist_ok=False)
    (out/'executed_source.py').write_bytes(Path(__file__).read_bytes())
    for name, expected in json.loads((run/'output_manifest.json').read_text()).items():
        assert digest(run/name) == expected
    provenance = json.loads((run/'provenance.json').read_text())
    cfg = provenance['config']
    baseline, price = ROOT/cfg['baseline_run'], ROOT/cfg['price_run']
    panels = dict(tuple(pd.read_csv(baseline/'monthly.csv').groupby(['sample', 'variant'])))
    models = {r['id']: r['columns'] for r in json.loads((baseline/'provenance.json').read_text())['config']['models']}
    scores = pd.read_csv(run/'forecast_diagnostics.csv')
    cases = pd.read_csv(run/'private_origin_diagnostics.csv')
    score_count, case_count = 0, 0
    grouping = ['sample', 'variant', 'model', 'horizon_months']
    for keys, group_scores in scores.groupby(grouping):
        sample, variant, model, horizon = keys
        panel = panels[sample, variant].reset_index(drop=True)
        columns = models[model]
        x = panel[columns].to_numpy(float)
        q = panel.discount_pp.to_numpy(float)
        target = panel.discount_pp.shift(-int(horizon)).to_numpy()-q
        grid = np.arange(len(panel))
        f = pd.read_csv(price/f'{sample}_{variant}_{model}_{horizon}_forecasts.csv')
        group_cases = cases[(cases['sample'] == sample) & (cases.variant == variant) &
                            (cases.model == model) & (cases.horizon_months == horizon)]
        for row in group_scores.itertuples():
            frame = f[(f.window == row.window) & (f.method == row.method)]
            c = group_cases[(group_cases.window == row.window) & (group_cases.method == row.method)]
            assert len(c) == len(frame) == row.forecast_n
            assert list(c.origin_month) == list(frame.origin_month)
            actual = frame.actual_change_pp.to_numpy()
            loss = (actual-frame.prediction_change_pp.to_numpy())**2
            persistence = np.mean(actual**2)
            historical = np.mean((actual-frame.training_mean_prediction.to_numpy())**2)
            assert np.allclose([row.model_mse, row.persistence_mse, row.training_mean_mse],
                               [loss.mean(), persistence, historical], rtol=1e-10, atol=1e-10)
            assert np.isclose(row.training_mean_to_persistence_mse, historical/persistence)
            assert row.wins_mean_only == (loss.mean() < historical and loss.mean() >= persistence)
            flags, qflags, bounds = [], [], []
            for case, forecast in zip(c.itertuples(), frame.itertuples()):
                origin = int(forecast.origin_grid)
                mask = ((grid < origin) & (grid+int(horizon) <= origin) &
                        np.isfinite(x).all(axis=1) & np.isfinite(target))
                if row.window == 'rolling120':
                    mask &= grid >= origin-120
                assert int(mask.sum()) == case.training_n
                outside = (x[origin] < np.min(x[mask], axis=0)) | (x[origin] > np.max(x[mask], axis=0))
                any_flag = bool(outside.any())
                discount_flag = bool(outside[columns.index('discount_pp')])
                terminal = q[origin]+forecast.prediction_change_pp
                bound = bool(terminal >= 100)
                assert case.feature_extrapolation == any_flag
                assert case.discount_extrapolation == discount_flag
                assert case.terminal_discount_at_or_above_100 == bound
                assert np.isclose(case.predicted_terminal_discount_pp, terminal, rtol=0, atol=1e-9)
                flags.append(any_flag); qflags.append(discount_flag); bounds.append(bound)
            assert row.feature_extrapolation_origins == sum(flags)
            assert row.discount_extrapolation_origins == sum(qflags)
            assert row.terminal_discount_at_or_above_100 == sum(bounds)
            flags = np.asarray(flags)
            if flags.any():
                assert np.isclose(row.extrapolation_mse, loss[flags].mean())
            if (~flags).any():
                assert np.isclose(row.within_training_range_mse, loss[~flags].mean())
            years = pd.PeriodIndex(frame.origin_month, freq='M').year
            shares = {int(year): float(loss[years == year].sum()) for year in set(years)}
            biggest = max(shares, key=shares.get)
            assert biggest == row.largest_loss_origin_year
            assert np.isclose(row.largest_origin_year_loss_share, shares[biggest]/loss.sum())
            score_count += 1; case_count += len(frame)
    translated = pd.read_csv(run/'drawdown_units_review.csv')
    legacy = pd.read_csv(ROOT/cfg['exception_trading_table']).set_index('pair')
    for row in translated.itertuples():
        field = 'gross_max_drawdown_pct' if row.scope == 'gross' else 'quoted_spread_net_max_drawdown_pct'
        value = legacy.loc[row.pair, field]
        assert np.isclose(row.legacy_field_value_log_points, value, equal_nan=True)
        assert np.isclose(row.geometric_index_drawdown_pct_same_legacy_peaks, 100*(np.exp(value/100)-1), equal_nan=True)
        assert not row.funded_portfolio_drawdown_established and not row.initial_zero_peak_reconstructed
    evidence = read(run/'source_review/evidence_admission.csv')
    new = ROOT/cfg['new_snapshot']
    new_facts = {r['fact_id']: r for r in read(new/'prepared/report_additional_facts.csv')}
    old_facts = {r['v3_record_id']: r for r in read(price/'source_review/evidence_admission.csv')}
    assert len(evidence) == 1991
    for row in evidence:
        assert row['forecast_feature_admitted'] == 'False'
        original = (new_facts[row['fact_id']] if row['v4_record_id'].startswith('loop_public_report_additions/')
                    else old_facts[row['v4_record_id']])
        assert all(row[field] == value for field, value in original.items())
    assert read(run/'source_review/report_availability_bounds.csv') == read(new/'prepared/novo_report_availability_clocks.csv')
    assert read(run/'source_review/revision_and_source_alerts.csv') == read(new/'prepared/revision_and_source_alerts.csv')
    for name, expected in provenance['protected_inputs'].items():
        assert digest(Path(name)) == expected
    summary = {'status': 'passed', 'score_diagnostics_verified': score_count,
        'origin_diagnostics_verified': case_count, 'drawdown_translations_verified': len(translated),
        'evidence_rows_preserved': len(evidence), 'availability_bounds_and_alerts_preserved': True,
        'prior_inputs_and_outputs_unchanged': True, 'new_model_fits': 0}
    (out/'AUDIT.json').write_text(json.dumps(summary, indent=2)+'\n')
    print(json.dumps(summary))


if __name__ == '__main__':
    main()
