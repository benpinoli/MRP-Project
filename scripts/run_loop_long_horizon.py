"""Tree-linked 24/60/120-month LOOP research. Follow BYU_ORC_AGENTS.md.

All licensed rows, fitted values and forecast origins stay in ignored runs/.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import sys
from datetime import datetime, timezone

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'src'))
from samsung_research.regressions import fit_ols


def digest(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as stream:
        for block in iter(lambda: stream.read(1024*1024), b''):
            h.update(block)
    return h.hexdigest()


def save_json(path, value):
    temporary = Path(str(path)+'.pending')
    temporary.write_text(json.dumps(value, indent=2, default=str, allow_nan=False)+'\n')
    temporary.replace(path)


def monthly_panel(daily, denominator, last_complete, fraction, minimum):
    """Ratio before averaging; preserve the entire calendar-month grid."""
    daily = daily.copy()
    daily['month'] = daily.date.dt.to_period('M')
    denominator = denominator.copy()
    denominator['month'] = denominator.date.dt.to_period('M')
    count = denominator.groupby('month').size()
    aggregate = daily.groupby('month').agg(discount_pp=('discount_pp', 'mean'),
        activity=('activity', 'mean'), valid_days=('discount_pp', 'count'),
        first_valid=('date', 'min'), last_valid=('date', 'max'))
    grid = pd.period_range(count.index.min(), pd.Period(last_complete, 'M'), freq='M')
    result = aggregate.reindex(grid)
    result['supplied_weekdays'] = count.reindex(grid).fillna(0).astype(int)
    result['valid_days'] = result.valid_days.fillna(0).astype(int)
    result['coverage_fraction'] = result.valid_days/result.supplied_weekdays.replace(0, np.nan)
    result['qualified'] = (result.valid_days >= minimum) & (result.coverage_fraction >= fraction)
    result.loc[~result.qualified, ['discount_pp', 'activity']] = np.nan
    result['trailing_12m_change'] = result.discount_pp-result.discount_pp.shift(12)
    result['grid'] = np.arange(len(result))
    result.index.name = 'month'
    return result


def labels(monthly, horizon):
    # The shift is over a complete calendar grid, never compressed valid rows.
    return monthly.discount_pp.shift(-horizon)-monthly.discount_pp


def eligible_training(monthly, y, columns, origin, horizon):
    valid = monthly[columns].notna().all(axis=1) & y.notna()
    # Month origin is fully completed. Equality allows an outcome whose last
    # completed month is the feature month; it is available at next-month origin.
    return valid & (monthly.grid < origin) & (monthly.grid+horizon <= origin)


def estimate(monthly, y, columns, mask, horizon, cfg):
    selected = monthly.loc[mask]
    x = np.column_stack([np.ones(len(selected)), selected[columns].to_numpy(float)])
    b, se, _, _, diag = fit_ols(y.loc[mask].to_numpy(float), x, selected.grid.to_numpy(int),
        horizon, minimum=cfg['minimum_training_observations'],
        observations_per_parameter=cfg['observations_per_parameter'])
    return b, se, diag


def fit_forecast(monthly, cfg, sample, variant):
    coefficients, predictions, statuses, current = [], [], [], []
    for horizon in cfg['horizons_months']:
        y = labels(monthly, horizon)
        endpoint_count = int(y.notna().sum())
        anchored = y.iloc[::horizon].dropna()
        for spec in cfg['models']:
            base = dict(sample=sample, variant=variant, model=spec['id'], horizon_months=horizon,
                        tree_nodes=';'.join(spec['tree_nodes']))
            complete = y.notna() & monthly[spec['columns']].notna().all(axis=1)
            status = {**base, 'endpoint_labels': endpoint_count,
                'anchored_nonoverlap_labels': len(anchored), 'complete_model_rows': int(complete.sum()),
                'full_fit': 'not_estimable', 'pseudo_oos_forecasts': 0, 'skipped_origins': 0}
            try:
                b, se, diag = estimate(monthly, y, spec['columns'], complete, horizon, cfg)
                status.update(full_fit='estimated', adjusted_r_squared=diag['adjusted_r_squared'],
                              standardized_condition=diag['standardized_condition'])
                for name, value, error in zip(['intercept']+spec['columns'], b, se):
                    coefficients.append({**base, 'term': name, 'coefficient': value,
                        'descriptive_hac_se': error, 'n': diag['n'], 'hac_months': horizon,
                        'confirmatory_inference': False})
            except ValueError as error:
                status['failure_reason'] = str(error)
            for origin in range(len(monthly)-horizon):
                if not complete.iloc[origin]:
                    continue
                train = eligible_training(monthly, y, spec['columns'], origin, horizon)
                try:
                    b, _, diag = estimate(monthly, y, spec['columns'], train, horizon, cfg)
                except ValueError:
                    status['skipped_origins'] += 1
                    continue
                x = np.r_[1., monthly.iloc[origin][spec['columns']].to_numpy(float)]
                newest_train = int(monthly.loc[train, 'grid'].max())
                assert newest_train+horizon <= origin
                predictions.append({**base, 'origin_month': str(monthly.index[origin]),
                    'available_origin_date': str((monthly.index[origin]+1).start_time.date()),
                    'target_month': str(monthly.index[origin+horizon]),
                    'origin_grid': origin, 'last_training_origin_grid': newest_train,
                    'latest_training_label_end_grid': newest_train+horizon,
                    'training_n': diag['n'], 'actual_change_pp': float(y.iloc[origin]),
                    'prediction_change_pp': float(x@b), 'zero_change_prediction': 0.,
                    'training_mean_prediction': float(y.loc[train].mean()),
                    'origin_discount_pp': float(monthly.iloc[origin].discount_pp),
                    'evaluation': 'retrospective_pseudo_oos_not_untouched'})
                status['pseudo_oos_forecasts'] += 1
            # Candidate future forecasts, fitted only on matured labels. They
            # are retained even when a horizon has no historical OOS support.
            origin = len(monthly)-1
            if origin >= 0 and monthly.iloc[origin][spec['columns']].notna().all():
                train = eligible_training(monthly, y, spec['columns'], origin, horizon)
                try:
                    b, _, diag = estimate(monthly, y, spec['columns'], train, horizon, cfg)
                    delta = float(np.r_[1., monthly.iloc[origin][spec['columns']].to_numpy(float)]@b)
                    current.append({**base, 'origin_month': str(monthly.index[origin]),
                        'target_month': str(monthly.index[origin]+horizon),
                        'origin_discount_pp': float(monthly.iloc[origin].discount_pp),
                        'candidate_change_pp': delta,
                        'candidate_terminal_discount_pp': float(monthly.iloc[origin].discount_pp+delta),
                        'training_n': diag['n'], 'validated_forecast': False,
                        'reason': 'Conditional linear candidate; exposed history, structural stability and vintage uncertainty remain'})
                except ValueError:
                    pass
            statuses.append(status)
    return coefficients, predictions, statuses, current


def evaluate(predictions):
    rows = []
    if predictions.empty:
        return pd.DataFrame()
    for keys, frame in predictions.groupby(['sample', 'variant', 'model', 'horizon_months']):
        actual = frame.actual_change_pp.to_numpy()
        error = actual-frame.prediction_change_pp.to_numpy()
        mse = np.mean(error**2)
        baseline = np.mean(actual**2)
        hist_mse = np.mean((actual-frame.training_mean_prediction.to_numpy())**2)
        # Nonoverlapping outcomes can share boundary observations, but not
        # interior holding periods. Record every possible phase separately.
        horizon = int(keys[3])
        phase_results = []
        for phase in range(horizon):
            sub = frame[frame.origin_grid % horizon == phase]
            if len(sub):
                base = np.mean(sub.actual_change_pp**2)
                loss = np.mean((sub.actual_change_pp-sub.prediction_change_pp)**2)
                phase_results.append((len(sub), 1-loss/base if base > 0 else np.nan))
        rows.append(dict(zip(['sample', 'variant', 'model', 'horizon_months'], keys)) | {
            'forecast_n': len(frame), 'first_origin': frame.origin_month.min(),
            'last_origin': frame.origin_month.max(), 'rmse_pp': np.sqrt(mse),
            'persistence_rmse_pp': np.sqrt(baseline), 'training_mean_rmse_pp': np.sqrt(hist_mse),
            'r2_vs_persistence': 1-mse/baseline if baseline > 0 else np.nan,
            'r2_vs_training_mean': 1-mse/hist_mse if hist_mse > 0 else np.nan,
            'mae_pp': np.mean(abs(error)),
            'max_nonoverlap_forecasts_in_one_phase': max(n for n, _ in phase_results),
            'evaluation_status': 'exploratory_dependent_exposed_history',
            'validated_predictive_model': False})
    return pd.DataFrame(rows)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--config', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    cfg = json.loads(args.config.read_text())
    out = args.output.resolve()
    if not out.is_relative_to(ROOT/'runs'):
        raise ValueError('Outputs must remain in ignored runs/')
    out.mkdir(parents=True, exist_ok=False, mode=0o700)
    save_json(out/'progress.json', {'status': 'started', 'completed_samples': []})
    review = ROOT/cfg['review_directory']
    member_path = review/'proposed_sample_membership.csv'
    if digest(member_path) != cfg['daily_membership_sha256']:
        raise ValueError('Daily candidate membership changed')
    summary = json.loads((review/'review_summary.json').read_text())
    manifest = json.loads((review/'review_manifest.json').read_text())
    for filename in ('proposed_sample_membership.csv', 'review_summary.json'):
        expected = next(r['sha256'] for r in manifest['files'] if r['path'] == filename)
        if digest(review/filename) != expected:
            raise ValueError('Review integrity failure')
    inputs = {str(member_path.relative_to(ROOT)): digest(member_path),
              str((review/'review_summary.json').relative_to(ROOT)): digest(review/'review_summary.json')}
    frame = pd.read_csv(member_path, dtype=str)
    frame['date'] = pd.to_datetime(frame.date)
    receipt_path = ROOT/'data/acquisition/2026-11-12/wrds_daily_and_mapping/prepared/crsp_us_receipts_daily_unique_prices_and_returns_for_review.csv'
    source_manifest = json.loads((receipt_path.parent.parent/'acquisition_manifest.json').read_text())
    receipt_expected = next(r['sha256'] for r in source_manifest['files']
                            if r['path'] == 'prepared/'+receipt_path.name)
    if digest(receipt_path) != receipt_expected:
        raise ValueError('Receipt source changed')
    inputs[str(receipt_path.relative_to(ROOT))] = receipt_expected
    receipt_volume = pd.read_csv(receipt_path, dtype={'PERMNO': str},
        usecols=['PERMNO', 'DlyCalDt', 'DlyVol'])
    receipt_volume['date'] = pd.to_datetime(receipt_volume.DlyCalDt)
    frame = frame.merge(receipt_volume[['PERMNO', 'date', 'DlyVol']],
        left_on=['us_PERMNO', 'date'], right_on=['PERMNO', 'date'], how='left', validate='many_to_one')
    fx_path = ROOT/cfg['fx_path']
    fx = pd.DataFrame()
    if fx_path.exists() and fx_path.stat().st_size:
        if digest(fx_path) != cfg['fx_sha256']:
            raise ValueError('Frozen FX input changed')
        inputs[cfg['fx_path']] = digest(fx_path)
        raw_fx = pd.read_csv(fx_path)
        if {'date', 'currency', 'foreign_units_per_EUR'} <= set(raw_fx):
            fx = raw_fx.pivot(index='date', columns='currency', values='foreign_units_per_EUR')
        else:
            fx = raw_fx.pivot(index='TIME_PERIOD', columns='CURRENCY', values='OBS_VALUE')
        fx.index = pd.to_datetime(fx.index)
        fx['EUR'] = 1.
        fx = fx.apply(pd.to_numeric, errors='coerce').where(lambda x: x > 0)
    by_sample = {s['sample']: s for s in summary['proposed_samples']}
    coefficient_rows, forecast_rows, status_rows, current_rows = [], [], [], []
    monthly_rows, coverage, daily_rows = [], [], []
    for sample, data in frame.groupby('sample', sort=True):
        data = data.sort_values('date').copy()
        spec = by_sample[sample]
        comparison = spec['comparison']
        outer_path = ROOT/'data/acquisition/2026-11-12/orc_nine_panel_review_20261112'/(comparison+'_review_panel.csv')
        outer = pd.read_csv(outer_path, usecols=['date'], parse_dates=['date'])
        inputs[str(outer_path.relative_to(ROOT))] = digest(outer_path)
        outer = outer[(outer.date.dt.weekday < 5) & outer.date.between(spec['start_bound_inclusive'], spec['end_bound_inclusive'])]
        receipt = spec['permno'] is not None
        left = pd.to_numeric(data.local_1_prccd)/pd.to_numeric(data.local_1_qunit)
        if receipt:
            right = pd.to_numeric(data.us_DlyClose)
            ratio_records = [r for r in summary['ratios'] if r['comparison'] == comparison]
            ratio = next(float(r['ordinary_shares_per_receipt']) for r in ratio_records
                         if comparison != 'alibaba' or float(r['ordinary_shares_per_receipt']) == 8)
            data['activity'] = np.log(pd.to_numeric(data.DlyVol)*ratio/pd.to_numeric(data.local_1_cshtrd))
            ccy = data.local_1_curcdd.iloc[0]
            if ccy not in fx or 'USD' not in fx:
                coverage.append({'sample': sample, 'status': 'blocked_missing_fx', 'currency': ccy})
                continue
            rate = (fx['USD']/fx[ccy]).reindex(data.date).to_numpy()
            # Positive discount = local equivalent cheaper than receipt.
            data['discount_pp'] = 100*(1-ratio*left*rate/right)
        else:
            right = pd.to_numeric(data.local_2_prccd)/pd.to_numeric(data.local_2_qunit)
            data['activity'] = np.log(pd.to_numeric(data.local_2_cshtrd)/pd.to_numeric(data.local_1_cshtrd))
            if comparison in ('byd', 'ping_an'):
                if 'CNY' not in fx or 'HKD' not in fx:
                    coverage.append({'sample': sample, 'status': 'blocked_missing_fx', 'currency': 'CNY/HKD'})
                    continue
                # A in CNY; H in HKD converted to CNY. Discount of H vs A.
                rate = (fx['CNY']/fx['HKD']).reindex(data.date).to_numpy()
                data['discount_pp'] = 100*(1-right*rate/left)
            else:
                data['discount_pp'] = 100*(1-right/left)
        data['discount_pp'] = data.discount_pp.where(np.isfinite(data.discount_pp))
        last_complete = cfg['last_complete_month_by_provider']['receipt' if receipt else 'local']
        # Source FX coverage can end earlier than the candidate security panel.
        # Keep missing FX visible; no interpolation/extrapolation.
        coverage.append({'sample': sample, 'status': 'estimated_candidates',
            'daily_candidates': len(data), 'daily_with_gap': int(data.discount_pp.notna().sum()),
            'discount_definition': '100*(1-cheaper_candidate/reference); no cost-of-capital identification',
            'ratio_assumption': ratio if receipt else 1,
            'synchronized_close': False if receipt or comparison in ('byd', 'ping_an') else 'same_market_proxy'})
        daily_rows.append(data[['sample', 'date', 'discount_pp', 'activity']])
        for variant, fraction in cfg['coverage_variants'].items():
            monthly = monthly_panel(data, outer, last_complete, fraction, cfg['minimum_monthly_observations'])
            monthly['sample'] = sample
            monthly['variant'] = variant
            monthly_rows.append(monthly.reset_index())
            co, pr, st, cu = fit_forecast(monthly, cfg, sample, variant)
            coefficient_rows.extend(co); forecast_rows.extend(pr); status_rows.extend(st); current_rows.extend(cu)
        # Each class gets a durable checkpoint before moving on.
        save_json(out/(sample+'_checkpoint.json'), {'status': 'completed', 'sample': sample})
        save_json(out/'progress.json', {'status': 'running', 'completed_samples': [r['sample'] for r in coverage]})
    for name, rows in [('coefficients', coefficient_rows), ('forecasts', forecast_rows),
                       ('model_status', status_rows), ('candidate_future_forecasts', current_rows), ('coverage', coverage)]:
        pd.DataFrame(rows).to_csv(out/(name+'.csv'), index=False)
    if monthly_rows:
        pd.concat(monthly_rows, ignore_index=True).to_csv(out/'monthly.csv', index=False)
    if daily_rows:
        pd.concat(daily_rows, ignore_index=True).to_csv(out/'daily_gap_diagnostics.csv', index=False)
    evaluation = evaluate(pd.DataFrame(forecast_rows))
    evaluation.to_csv(out/'evaluation.csv', index=False)
    forecast_frame = pd.DataFrame(forecast_rows)
    incremental = []
    if not forecast_frame.empty:
        join = ['sample', 'variant', 'horizon_months', 'origin_month']
        for base_model, extended_model in [('LH-LEVEL', 'LH-STATE'), ('LH-STATE', 'LH-ACTIVITY')]:
            base = forecast_frame[forecast_frame.model == base_model]
            extended = forecast_frame[forecast_frame.model == extended_model]
            matched = base.merge(extended, on=join, suffixes=('_base', '_extended'), validate='one_to_one')
            for keys, g in matched.groupby(['sample', 'variant', 'horizon_months']):
                base_loss = np.mean((g.actual_change_pp_base-g.prediction_change_pp_base)**2)
                extended_loss = np.mean((g.actual_change_pp_base-g.prediction_change_pp_extended)**2)
                incremental.append(dict(zip(['sample', 'variant', 'horizon_months'], keys)) | {
                    'base_model': base_model, 'extended_model': extended_model,
                    'common_forecasts': len(g), 'base_rmse_pp': np.sqrt(base_loss),
                    'extended_rmse_pp': np.sqrt(extended_loss),
                    'incremental_r2': 1-extended_loss/base_loss if base_loss > 0 else np.nan,
                    'causal_mechanism_identified': False})
    pd.DataFrame(incremental).to_csv(out/'incremental_comparisons.csv', index=False)
    for relative, expected in inputs.items():
        if digest(ROOT/relative) != expected:
            raise ValueError('Input changed during run: '+relative)
    save_json(out/'provenance.json', {'config': cfg, 'config_sha256': digest(args.config),
        'code_sha256': digest(Path(__file__)), 'regression_engine_sha256': digest(ROOT/'src/samsung_research/regressions.py'),
        'inputs': inputs, 'python': sys.version, 'numpy': np.__version__, 'pandas': pd.__version__,
        'slurm_job_id': os.environ.get('SLURM_JOB_ID'), 'completed_utc': datetime.now(timezone.utc).isoformat(),
        'limitations': cfg['known_limitations'], 'validated_predictive_model': False})
    save_json(out/'progress.json', {'status': 'completed', 'samples': len(coverage),
        'model_status_rows': len(status_rows), 'pseudo_oos_forecasts': len(forecast_rows),
        'completed_utc': datetime.now(timezone.utc).isoformat()})
    print(json.dumps({'samples': len(coverage), 'models_estimated': sum(s['full_fit'] == 'estimated' for s in status_rows),
                      'forecasts': len(forecast_rows), 'validated_predictive_models': 0}))


if __name__ == '__main__':
    main()
