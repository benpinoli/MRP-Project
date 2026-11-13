"""Verify LH2 aggregates and reproduce receipt audits privately. See BYU_ORC_AGENTS.md."""
import argparse
import json
from pathlib import Path
import shutil
import subprocess
import sys

import numpy as np
import pandas as pd

from verify_loop_deliveries import digest, verify_receipts

ROOT = Path(__file__).resolve().parents[1]


def check_score(row, frame):
    assert len(frame) == row.forecast_n
    y = frame.actual_change_pp.to_numpy()
    mse = np.mean((y-frame.prediction_change_pp.to_numpy())**2)
    base = np.mean(y*y)
    mean_loss = np.mean((y-frame.training_mean_prediction.to_numpy())**2)
    assert np.isclose(np.sqrt(mse), row.rmse_pp, rtol=0, atol=1e-9)
    assert np.isclose(1-mse/base, row.r2_vs_persistence, rtol=1e-10, atol=1e-9)
    assert np.isclose(1-mse/mean_loss, row.r2_vs_training_mean, rtol=1e-10, atol=1e-9)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--run', type=Path, required=True)
    parser.add_argument('--verification-name', default='verification')
    parser.add_argument('--reuse-daily-audit', type=Path)
    args = parser.parse_args()
    run = args.run.resolve()
    assert run.is_relative_to(ROOT/'runs')
    assert Path(args.verification_name).name == args.verification_name
    out = run/args.verification_name
    out.mkdir(mode=0o700, exist_ok=False)
    (out/'executed_source.py').write_bytes(Path(__file__).read_bytes())
    for name, expected in json.loads((run/'output_manifest.json').read_text()).items():
        assert digest(run/name) == expected
    receipts = verify_receipts(out)
    cfg = json.loads((run/'provenance.json').read_text())['config']
    baseline = ROOT/cfg['baseline_run']
    baseline_f = pd.read_csv(baseline/'forecasts.csv')
    count = 0
    for name in ('scores', 'nonoverlap_phases', 'calendar_periods'):
        rows = pd.read_csv(run/(name+'.csv'))
        for keys, group in rows.groupby(['sample', 'variant', 'model', 'horizon_months']):
            sample, variant, model, horizon = keys
            f = pd.read_csv(run/f'{sample}_{variant}_{model}_{horizon}_forecasts.csv')
            for row in group.itertuples():
                sub = f[f.method == row.method]
                if name == 'nonoverlap_phases':
                    sub = sub[sub.origin_grid % int(horizon) == row.phase]
                    assert (np.diff(sub.origin_grid) >= int(horizon)).all()
                elif name == 'calendar_periods':
                    lo, hi = next((lo, hi) for label, lo, hi in cfg['calendar_periods'] if label == row.period)
                    years = pd.PeriodIndex(sub.origin_month, freq='M').year
                    sub = sub[(years >= lo) & (years <= hi)]
                check_score(row, sub)
                count += 1
            if name == 'scores':
                old = baseline_f[(baseline_f['sample'] == sample) & (baseline_f.variant == variant) &
                                 (baseline_f.model == model) & (baseline_f.horizon_months == horizon)]
                for method in ('OLS', 'RIDGE'):
                    sub = f[f.method == method]
                    assert list(sub.origin_month) == list(old.origin_month)
                    assert np.allclose(sub.actual_change_pp, old.actual_change_pp)
                original = f[f.method == 'OLS'].prediction_change_pp.to_numpy()
                assert np.allclose(original, old.prediction_change_pp, atol=1e-7, rtol=0)
    drift = pd.read_csv(run/'coefficient_drift.csv')
    for keys, group in drift.groupby(['sample', 'variant', 'model', 'horizon_months']):
        sample, variant, model, horizon = keys
        coefficients = pd.read_csv(run/f'{sample}_{variant}_{model}_{horizon}_coefficients.csv')
        for row in group.itertuples():
            c = coefficients[(coefficients.method == row.method) & (coefficients.term == row.term)].coefficient.to_numpy()
            assert len(c) == row.origin_n
            assert np.allclose([c[0], c[-1], c.min(), c.max()],
                               [row.first_coefficient, row.last_coefficient, row.minimum, row.maximum])
            assert int(np.sum(np.sign(c[1:]) != np.sign(c[:-1]))) == row.sign_transitions
    increments = pd.read_csv(run/'incremental.csv')
    for row in increments.itertuples():
        a, b = [pd.read_csv(run/f'{row.sample}_{row.variant}_{model}_{row.horizon_months}_forecasts.csv')
                for model in (row.simpler, row.larger)]
        f = a[a.method == row.method].merge(b[b.method == row.method], on='origin_month', suffixes=('_a','_b'))
        assert len(f) == row.common_origins
        loss_a = np.mean((f.actual_change_pp_a-f.prediction_change_pp_a)**2)
        loss_b = np.mean((f.actual_change_pp_b-f.prediction_change_pp_b)**2)
        assert np.isclose(1-loss_b/loss_a, row.incremental_r2)
    # Audit a private copy because the portable script regenerates prepared files.
    source = ROOT/'data/acquisition/2026-11-12/wrds_daily_and_mapping'
    copy = args.reuse_daily_audit.resolve() if args.reuse_daily_audit else out/'daily_audit_copy'
    assert copy.is_relative_to(run)
    if args.reuse_daily_audit:
        # Reuse only a completed audit of these exact raw sources; preserve the
        # earlier failed verification directory and its successful audit log.
        assert (copy.parent/'portable_daily_audit.log').is_file()
        assert digest(copy/'audit_acquisition.py') == digest(source/'audit_acquisition.py')
        for path in (source/'raw').iterdir():
            if path.is_file():
                assert digest(copy/'raw'/path.name) == digest(path)
    else:
        shutil.copytree(source, copy)
        with (out/'portable_daily_audit.log').open('w') as log:
            subprocess.run([sys.executable, str(copy/'audit_acquisition.py')], check=True, stdout=log, stderr=subprocess.STDOUT)
    assert json.loads((copy/'prepared/validation_summary.json').read_text()) == json.loads((source/'prepared/validation_summary.json').read_text())
    descriptor = out/'descriptor_audit_copy'
    shutil.copytree(ROOT/'data/acquisition/2026-11-11/wrds_descriptor_review', descriptor)
    with (out/'descriptor_review.log').open('w') as log:
        subprocess.run([sys.executable, str(ROOT/'scripts/review_wrds_crosswalk.py'), '--bundle',
            str(descriptor), '--output', str(descriptor/'v2_identity_review')],
            check=True, stdout=log, stderr=subprocess.STDOUT)
    actual = json.loads((descriptor/'v2_identity_review/review_summary.json').read_text())
    delivered = json.loads((descriptor/'identity_review/review_summary.json').read_text())
    for field in ('identity_decisions', 'verified_raw_rows', 'verified_source_exports', 'reviewed_candidate_records'):
        assert actual[field] == delivered[field]
    for relative, expected in json.loads((baseline/'provenance.json').read_text())['inputs'].items():
        assert digest(ROOT/relative) == expected
    for name, expected in json.loads((baseline/'verification/AUDIT.json').read_text())['original_output_sha256'].items():
        assert digest(baseline/name) == expected
    summary = {'status':'passed', 'aggregate_score_rows_verified': count,
        'drift_rows_verified': len(drift), 'incremental_rows_verified': len(increments),
        'same_origins_verified': True, 'portable_daily_audit_matches_delivery': True,
        'descriptor_review_passed': True, 'baseline_and_inputs_unchanged': True,
        'independent_agent_review': False}
    (out/'AUDIT.json').write_text(json.dumps(summary, indent=2)+'\n')
    print(json.dumps(summary))


if __name__ == '__main__':
    main()
