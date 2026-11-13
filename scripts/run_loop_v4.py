"""Read-only installed-source and existing-forecast diagnostics. See BYU_ORC_AGENTS.md."""
import argparse
import json
import os
from pathlib import Path
import subprocess
from collections import Counter

import numpy as np
import pandas as pd

from audit_loop_v3_sources import read, write, verify_reference, known_date, checked_hash
from check_loop_stability import save
from verify_loop_deliveries import digest, safe_name

ROOT = Path(__file__).resolve().parents[1]


def source_review(cfg, out):
    stage = ROOT/cfg['stage_directory']
    index = json.loads((stage/'BUNDLE_INDEX.json').read_text())
    installed = 0
    snapshots = []
    for bundle in index:
        target = ROOT/bundle['target_relative_directory']
        delivery = json.loads((stage/bundle['delivery_json']).read_text())
        assert len(delivery['files']) == bundle['inner_entries']
        for row in delivery['files']:
            safe_name(row['path'])
            p = target/row['path']
            assert p.resolve().is_relative_to(target.resolve()) and not p.is_symlink()
            assert p.stat().st_size == row.get('bytes', row.get('size'))
            assert checked_hash(p) == row['sha256'], str(p)
            installed += 1
        snapshots.append({'snapshot': bundle['snapshot'], 'entries': len(delivery['files']), 'installed_bytes_verified': True})
    assert installed == 600
    base = ROOT/'data/acquisition/2026-11-12'
    refs = []
    for path in (base/'loop_long_horizon_followup/inputs/reused_source_references.json',
                 base/'loop_gap_closure_supplement/inputs/annual_source_references.json',
                 base/'loop_gap_closure_supplement/prepared/prerequisite_source_references.json',
                 base/'loop_public_report_additions/inputs/reused_source_references.json'):
        for row in json.loads(path.read_text()):
            verify_reference(row['path'], row['sha256'])
            refs.append(row)
    new = ROOT/cfg['new_snapshot']
    facts = read(new/'prepared/report_additional_facts.csv')
    clocks = read(new/'prepared/novo_report_availability_clocks.csv')
    alerts = read(new/'prepared/revision_and_source_alerts.csv')
    inventory = read(new/'prepared/source_inventory.csv')
    passages = {p['passage_id']: p for p in json.loads((new/'prepared/source_passages.json').read_text())}
    checks = read(new/'prepared/extraction_checks.csv')
    excluded = read(new/'prepared/excluded_previously_transcribed.csv')
    assert len(facts) == len({r['fact_id'] for r in facts}) == 616
    assert Counter(r['issuer'] for r in facts) == {'VW': 257, 'Novo': 201, 'Hyundai': 158}
    assert len(clocks) == 4 and len(alerts) == 8 and len(inventory) == 59 and len(excluded) == 59
    assert len(checks) == 47 and all(r['status'] == 'pass' for r in checks)
    for row in inventory:
        verify_reference(row['path'], row['sha256'])
    new_admission = []
    for row in facts:
        for field in ('issuer', 'security_class', 'observation_date', 'effective_date', 'first_public_release_date',
                      'retrieved_at', 'field', 'value', 'unit', 'status', 'source_file', 'source_sha256', 'locator', 'vintage'):
            assert row[field].strip(), (row['fact_id'], field)
        resolved = verify_reference(row['source_file'], row['source_sha256'], new)
        assert row['source_passage_id'] in passages
        assert passages[row['source_passage_id']]['source_file'] == row['source_file']
        new_admission.append({**row, 'v4_record_id': 'loop_public_report_additions/'+row['fact_id'],
            'publication_date_known': known_date(row['first_public_release_date']),
            'forecast_feature_admitted': False, 'resolved_source_file': resolved,
            'v4_gate': 'Dated evidence only; preserve revisions, nominal/split basis, component/status and report-availability bounds; no structural predictor in this diagnostic'})
    for row in clocks:
        verify_reference(row['release_source_file'], row['release_sha256'])
        verify_reference(row['report_source_file'], row['report_sha256'])
        assert row['first_public_release_date'].startswith('unknown')
        assert not known_date(row['first_public_release_date'])
        assert known_date(row['availability_bound_date'])
    old_admission = read(ROOT/cfg['price_run']/'source_review/evidence_admission.csv')
    combined = [{**r, 'v4_record_id': r['v3_record_id']} for r in old_admission]+new_admission
    assert len(combined) == len({r['v4_record_id'] for r in combined}) == 1991
    assert all(str(r['forecast_feature_admitted']).lower() == 'false' for r in combined)
    write(out/'evidence_admission.csv', combined)
    write(out/'report_availability_bounds.csv', clocks)
    write(out/'revision_and_source_alerts.csv', alerts)
    write(out/'new_coverage_matrix.csv', read(new/'prepared/coverage_matrix.csv'))
    summary = {'installed_snapshots': snapshots, 'installed_entries_verified': installed,
        'reused_reference_records_verified': len(refs), 'new_facts': len(facts),
        'new_unknown_first_publication': sum(not known_date(r['first_public_release_date']) for r in facts),
        'combined_facts': len(combined),
        'combined_unknown_first_publication': sum(not known_date(r['first_public_release_date']) for r in combined),
        'availability_bounds_retained_separately': len(clocks), 'revision_alerts_retained': len(alerts),
        'source_inventory_rows': len(inventory), 'extraction_checks': len(checks),
        'prior_exact_transcriptions_excluded_by_delivery': len(excluded),
        'new_paired_intervals_admitted': 0, 'structural_forecast_features_admitted': 0}
    save(out/'source_audit.json', summary)
    return summary


def geometric_drawdown_translation(legacy_log_points):
    return 100*np.expm1(np.asarray(legacy_log_points)/100)


def synthetic_checks():
    assert np.isclose(geometric_drawdown_translation(-100*np.log(2)), -50)
    assert np.isclose(geometric_drawdown_translation(0), 0)
    assert -100 < geometric_drawdown_translation(-238.1755) < 0
    # Positive-price discount has a one-sided upper bound; no lower bound.
    q = 100*(1-np.array([.2, 1., 4.]))
    assert np.all(q < 100) and q[-1] == -300
    # Beating a weak mean benchmark need not beat persistence.
    actual = np.array([1., -1.]); prediction = np.array([3., -3.]); mean = np.array([5., 5.])
    assert np.mean((actual-prediction)**2) > np.mean(actual**2)
    assert np.mean((actual-prediction)**2) < np.mean((actual-mean)**2)
    return 5


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
    checks = synthetic_checks()
    baseline, v2, v3 = [ROOT/cfg[k] for k in ('baseline_run', 'stability_run', 'price_run')]
    original = json.loads((baseline/'verification/AUDIT.json').read_text())['original_output_sha256']
    protected = {str(baseline/name): expected for name, expected in original.items()}
    for prior in (v2, v3):
        protected.update({str(prior/name): expected for name, expected in json.loads((prior/'output_manifest.json').read_text()).items()})
    protected.update({str(ROOT/name): expected for name, expected in json.loads((baseline/'provenance.json').read_text())['inputs'].items()})
    protected[str(ROOT/cfg['exception_trading_table'])] = digest(ROOT/cfg['exception_trading_table'])
    for name, expected in protected.items():
        assert digest(Path(name)) == expected
    source_dir = out/'source_review'
    source_dir.mkdir(mode=0o700)
    source = source_review(cfg, source_dir)
    save(out/'progress.json', {'status': 'sources_verified'})
    panels = dict(tuple(pd.read_csv(baseline/'monthly.csv').groupby(['sample', 'variant'])))
    prior_cfg = json.loads((baseline/'provenance.json').read_text())['config']
    models = {m['id']: m['columns'] for m in prior_cfg['models']}
    scores = pd.read_csv(v3/'scores.csv')
    diagnostics, private_cases = [], []
    for keys, score_group in scores.groupby(['sample', 'variant', 'model', 'horizon_months']):
        sample, variant, model, horizon = keys
        panel = panels[sample, variant].reset_index(drop=True)
        dates = pd.PeriodIndex(panel.month, freq='M')
        q = panel.discount_pp.to_numpy(float)
        assert np.all(q[np.isfinite(q)] < 100)
        y = panel.discount_pp.shift(-int(horizon)).to_numpy()-q
        x = panel[models[model]].to_numpy(float)
        complete = np.isfinite(x).all(axis=1) & np.isfinite(y)
        frame = pd.read_csv(v3/f'{sample}_{variant}_{model}_{horizon}_forecasts.csv')
        for (window, method), group in frame.groupby(['window', 'method']):
            flags, discount_flags, impossible = [], [], []
            for row in group.itertuples():
                origin = int(row.origin_grid)
                train = complete & (dates < dates[origin]) & (dates+int(horizon) <= dates[origin])
                if window == 'rolling120':
                    train &= dates >= dates[origin]-120
                assert int(train.sum()) == row.training_n
                minimum, maximum = x[train].min(axis=0), x[train].max(axis=0)
                outside = (x[origin] < minimum) | (x[origin] > maximum)
                flags.append(bool(outside.any()))
                discount_flags.append(bool(outside[models[model].index('discount_pp')]))
                terminal = q[origin]+row.prediction_change_pp
                impossible.append(bool(terminal >= 100))
                private_cases.append({'sample': sample, 'variant': variant, 'model': model,
                    'horizon_months': int(horizon), 'window': window, 'method': method,
                    'origin_month': row.origin_month, 'target_month': row.target_month,
                    'training_n': int(row.training_n), 'feature_extrapolation': bool(outside.any()),
                    'discount_extrapolation': discount_flags[-1], 'predicted_terminal_discount_pp': terminal,
                    'terminal_discount_at_or_above_100': impossible[-1]})
            actual = group.actual_change_pp.to_numpy()
            losses = (actual-group.prediction_change_pp.to_numpy())**2
            persistence = actual**2
            mean_losses = (actual-group.training_mean_prediction.to_numpy())**2
            years = pd.PeriodIndex(group.origin_month, freq='M').year
            yearly = pd.Series(losses).groupby(years).sum()
            flags = np.asarray(flags)
            base = {'sample': sample, 'variant': variant, 'model': model, 'horizon_months': int(horizon),
                    'window': window, 'method': method}
            old_score = score_group[(score_group.window == window) & (score_group.method == method)].iloc[0]
            r2_p = 1-losses.mean()/persistence.mean()
            r2_m = 1-losses.mean()/mean_losses.mean()
            assert np.isclose(r2_p, old_score.r2_vs_persistence) and np.isclose(r2_m, old_score.r2_vs_training_mean)
            diagnostics.append({**base, 'forecast_n': len(group), 'model_mse': losses.mean(),
                'persistence_mse': persistence.mean(), 'training_mean_mse': mean_losses.mean(),
                'r2_vs_persistence': r2_p, 'r2_vs_training_mean': r2_m,
                'training_mean_to_persistence_mse': mean_losses.mean()/persistence.mean(),
                'wins_persistence': r2_p > 0, 'wins_training_mean': r2_m > 0,
                'wins_mean_only': r2_m > 0 and r2_p <= 0,
                'feature_extrapolation_origins': int(flags.sum()), 'discount_extrapolation_origins': sum(discount_flags),
                'extrapolation_mse': losses[flags].mean() if flags.any() else np.nan,
                'within_training_range_mse': losses[~flags].mean() if (~flags).any() else np.nan,
                'terminal_discount_at_or_above_100': sum(impossible),
                'largest_origin_year_loss_share': yearly.max()/losses.sum() if losses.sum() else np.nan,
                'largest_loss_origin_year': int(yearly.idxmax())})
        save(out/'progress.json', {'status': 'forecast_diagnostics_running', 'last_group': list(keys),
                                   'completed_score_rows': len(diagnostics)})
    pd.DataFrame(diagnostics).to_csv(out/'forecast_diagnostics.csv', index=False)
    pd.DataFrame(private_cases).to_csv(out/'private_origin_diagnostics.csv', index=False)
    legacy = pd.read_csv(ROOT/cfg['exception_trading_table'])
    translated = []
    for row in legacy.to_dict('records'):
        for scope, column in [('gross', 'gross_max_drawdown_pct'), ('quoted_spread_net', 'quoted_spread_net_max_drawdown_pct')]:
            translated.append({'pair': row['pair'], 'scope': scope,
                'legacy_field_value_log_points': row[column],
                'geometric_index_drawdown_pct_same_legacy_peaks': float(geometric_drawdown_translation(row[column])),
                'funded_portfolio_drawdown_established': False, 'initial_zero_peak_reconstructed': False,
                'qualification': 'Dimensional translation of cumulative log-score index only; same legacy peak convention. Original did not prepend zero; no executable fills, funded portfolio or full costs certified.'})
    pd.DataFrame(translated).to_csv(out/'drawdown_units_review.csv', index=False)
    for name, expected in protected.items():
        assert digest(Path(name)) == expected
    for name in ('run_loop_v4.py', 'audit_loop_v3_sources.py'):
        (out/('executed_'+name)).write_bytes((ROOT/'scripts'/name).read_bytes())
    save(out/'provenance.json', {'config': cfg, 'config_sha256': digest(args.config),
        'code_sha256': digest(Path(__file__)), 'protected_inputs': protected,
        'git_head': subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip(),
        'numpy': np.__version__, 'pandas': pd.__version__, 'slurm_job_id': os.environ.get('SLURM_JOB_ID')})
    summary = {'status': 'completed', 'source_audit': source, 'forecast_score_rows': len(diagnostics),
        'forecast_origin_diagnostic_rows': len(private_cases), 'mean_only_win_rows': int(sum(r['wins_mean_only'] for r in diagnostics)),
        'forecast_terminal_bound_violations': sum(r['terminal_discount_at_or_above_100'] for r in diagnostics),
        'drawdown_translation_rows': len(translated), 'synthetic_checks': checks,
        'baseline_v2_v3_unchanged': True, 'new_model_fits': 0, 'validated_predictive_model': False}
    save(out/'summary.json', summary)
    save(out/'output_manifest.json', {str(p.relative_to(out)): digest(p) for p in out.rglob('*') if p.is_file() and p.name != 'progress.json'})
    save(out/'progress.json', summary)
    print((out/'summary.json').read_text())


if __name__ == '__main__':
    main()
