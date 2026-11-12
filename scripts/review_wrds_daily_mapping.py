"""Review the private daily snapshot without editing delivered files.

Follow BYU_ORC_AGENTS.md. Run the full review in Slurm; all outputs are private.
No regressions, FX downloads, provider splices, or job restarts are performed.
"""
import argparse
import csv
import hashlib
import json
import math
import shutil
import stat
import subprocess
import sys
import zipfile
from collections import Counter, defaultdict
from datetime import date, timedelta
from pathlib import Path, PurePosixPath, PureWindowsPath
from statistics import median


def digest(path):
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def safe_path(value):
    p = PurePosixPath(value)
    if (not value or '\\' in value or p.is_absolute() or
            PureWindowsPath(value).drive or any(x in ('', '.', '..') for x in value.split('/'))):
        raise ValueError('Unsafe package path: ' + value)
    return Path(*p.parts)


def verify_inventory(root, records):
    seen = set()
    for item in records:
        rel = safe_path(item['path'])
        if rel in seen:
            raise ValueError('Duplicate inventory path')
        seen.add(rel)
        path = root / rel
        if any(p.is_symlink() for p in [path, *path.parents] if p != root.parent):
            raise ValueError('Symlink in delivered path')
        if not path.resolve().is_relative_to(root.resolve()):
            raise ValueError('Path escapes snapshot')
        if not path.is_file() or ('size' in item and path.stat().st_size != item['size']):
            raise ValueError('Missing or wrong-sized file: ' + str(rel))
        if digest(path) != item['sha256']:
            raise ValueError('Hash mismatch: ' + str(rel))
    return len(seen)


def verify_zip(archive, delivery):
    if archive.stat().st_size != delivery['size'] or digest(archive) != delivery['sha256']:
        raise ValueError('ZIP size/hash mismatch')
    expected = {x['path']: x for x in delivery['files']}
    if len(expected) != len(delivery['files']):
        raise ValueError('Duplicate delivered path')
    with zipfile.ZipFile(archive) as zipped:
        names = set()
        for info in zipped.infolist():
            safe_path(info.filename)
            if info.is_dir() or stat.S_ISLNK(info.external_attr >> 16):
                raise ValueError('Unexpected directory/symlink ZIP entry')
            if info.filename in names or info.filename not in expected:
                raise ValueError('Duplicate or unexpected ZIP entry')
            names.add(info.filename)
            wanted = expected[info.filename]
            h = hashlib.sha256()
            with zipped.open(info) as stream:
                for block in iter(lambda: stream.read(1024 * 1024), b''):
                    h.update(block)
            if info.file_size != wanted['size'] or h.hexdigest() != wanted['sha256']:
                raise ValueError('ZIP member differs from inventory')
        if names != set(expected):
            raise ValueError('ZIP entry inventory mismatch')
    return len(names)


def read(path):
    with path.open(encoding='utf-8-sig', newline='') as stream:
        yield from csv.DictReader(stream)


def write(path, rows, fields=None):
    rows = list(rows)
    fields = fields or list(dict.fromkeys(k for row in rows for k in row))
    with path.open('x', newline='') as stream:
        w = csv.DictWriter(stream, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)


def number(value):
    try:
        value = float(value)
        return value if math.isfinite(value) else None
    except (ValueError, TypeError):
        return None


def positive(value):
    return number(value) is not None and number(value) > 0


def local_candidate(row):
    # This is an explicit conservative SCREEN, not a certification of PRCSTD.
    return (row['prcstd'] == '10' and row['mapping_count'] == '1' and
            positive(row['prccd']) and positive(row['cshtrd']) and
            bool(row['curcdd']) and positive(row['qunit']))


def us_candidate(row):
    return (row['PrimaryExch'] == 'N' and row['DlyPrcFlg'] == 'TR' and
            row['TradingStatusFlg'] == 'A' and row['ConditionalType'] == 'RW' and
            positive(row['DlyClose']) and positive(row['DlyVol']))


def spans(dates):
    return {'rows': len(dates), 'first': min(dates) if dates else None,
            'last': max(dates) if dates else None}


def same_symbol(left, right):
    return left.replace('.', '') == right.replace('.', '')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--bundle', type=Path, required=True)
    parser.add_argument('--descriptor', type=Path, required=True)
    parser.add_argument('--archive', type=Path, required=True)
    parser.add_argument('--delivery', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--rules', type=Path, default=Path(__file__).resolve().parents[1]/'configs/loop_daily_review_rules_20261112.json')
    args = parser.parse_args()
    b, descriptor, out = args.bundle.resolve(), args.descriptor.resolve(), args.output.resolve()
    if not out.is_relative_to(b.parent) or out == b or out.is_relative_to(b):
        raise ValueError('Use a new sibling directory in private acquisition storage')
    if out.exists():
        raise ValueError('Output exists; never overlay a prior review')
    delivery = json.loads(args.delivery.read_text())
    zip_count = verify_zip(args.archive, delivery)
    delivery_count = verify_inventory(b, delivery['files'])
    manifest = json.loads((b/'acquisition_manifest.json').read_text())
    manifest_count = verify_inventory(b, manifest['files'])
    identifier_rows = sum(1 for _ in read(b/'raw/compustat_security_identifier_history_9_issuers.csv'))
    if identifier_rows != 461:
        raise ValueError('Historical identifier row control failed')
    descriptor_manifest = json.loads((descriptor/'manifest.json').read_text())
    # The November 11 manifest was produced on Windows. Normalize only its
    # documented path separator; archive paths remain strict POSIX paths.
    descriptor_files = [{**r, 'path': r['path'].replace('\\', '/')} for r in descriptor_manifest['files']]
    verify_inventory(descriptor, descriptor_files)
    before_descriptor = digest(descriptor/'manifest.json')
    out.mkdir(mode=0o700)
    # The portable audit writes relative to __file__. Give it an isolated copy,
    # read-only source links, and only the prepared seed it actually requires.
    audit = out/'audit_reproduction'
    audit.mkdir()
    shutil.copyfile(b/'audit_acquisition.py', audit/'audit_acquisition.py')
    (audit/'raw').symlink_to(b/'raw', target_is_directory=True)
    (audit/'prepared').mkdir()
    shutil.copyfile(b/'prepared/local_acquisition_identity_intervals.csv',
                    audit/'prepared/local_acquisition_identity_intervals.csv')
    with (out/'portable_audit.log').open('x') as stream:
        subprocess.run([sys.executable, str(audit/'audit_acquisition.py')],
                       check=True, stdout=stream, stderr=subprocess.STDOUT)
    supplied = json.loads((b/'prepared/validation_summary.json').read_text())
    reproduced = json.loads((audit/'prepared/validation_summary.json').read_text())
    if supplied != reproduced:
        raise ValueError('Portable audit aggregate controls differ from delivery')
    reproduction = []
    for path in sorted((audit/'prepared').iterdir()):
        reproduction.append({'file': path.name, 'byte_identical': digest(path) == digest(b/'prepared'/path.name)})
    local = defaultdict(dict)
    intervals = defaultdict(list)
    for row in read(b/'prepared/local_acquisition_identity_intervals.csv'):
        intervals[row['gvkey'], row['iid']].append(row)
    for row in read(b/'prepared/local_requested_daily_with_dated_isin_for_review.csv'):
        key = row['gvkey'], row['iid']
        if row['datadate'] in local[key]:
            raise ValueError('Duplicate local date')
        local[key][row['datadate']] = row
    master = list(read(b/'inputs/exact_local_current_master_matches.csv'))
    public = list(read(b/'inputs/loop_security_descriptor_candidates.csv'))
    transitions = list(read(descriptor/'prepared/market_transition_dates_for_review.csv'))
    rules = json.loads(args.rules.read_text())
    transitions.extend(rules['supplemental_transition_windows'])
    ratios = list(read(descriptor/'prepared/receipt_ratio_evidence_and_basis_intervals.csv'))
    us = defaultdict(dict)
    flag_counts = defaultdict(Counter)
    for row in read(b/'prepared/crsp_us_receipts_daily_unique_prices_and_returns_for_review.csv'):
        us[row['PERMNO']][row['DlyCalDt']] = row
        for field in ('DlyPrcFlg', 'DlyRetDurFlg', 'TradingStatusFlg', 'ConditionalType', 'TradingSymbol'):
            flag_counts[row['PERMNO']][field+'='+row[field]] += 1
    # Dated CRSP identity decisions supply private keys; never embed a public crosswalk.
    identities = list(read(descriptor/'ssh_identity_review_20261112/reviewed_security_identities.csv'))
    receipts = defaultdict(set)
    for row in identities:
        if row['permno']:
            receipts[row['comparison']].add(row['permno'])
    extensions = defaultdict(dict)
    for row in read(b/'prepared/us_receipts_compustat_extension_with_overlap_for_review.csv'):
        extensions[row['matched_crsp_permno']][row['datadate']] = row
    metrics, gaps, exceptions, missing, adjustment, boundary_diagnostics = [], [], [], [], [], []
    for key, days in sorted(local.items()):
        rr = [days[d] for d in sorted(days)]
        comparison = intervals[key][0]['comparison']
        valid = [r['datadate'] for r in rr if positive(r['prccd'])]
        candidates = [r['datadate'] for r in rr if local_candidate(r)]
        metrics.append({'comparison': comparison, 'gvkey': key[0], 'iid': key[1],
            **spans(list(days)), 'first_positive': min(valid) if valid else None,
            'last_positive': max(valid) if valid else None,
            'screened': spans(candidates), 'status': dict(Counter(r['prcstd'] for r in rr)),
            'volume_missing': sum(number(r['cshtrd']) is None for r in rr),
            'volume_zero': sum(number(r['cshtrd']) == 0 for r in rr),
            'currencies': sorted({r['curcdd'] for r in rr}),
            'units': sorted({r['qunit'] for r in rr}),
            'weekend_rows': sum(date.fromisoformat(r['datadate']).weekday() >= 5 for r in rr)})
        status_diagnostics = defaultdict(Counter)
        for n, row in enumerate(rr):
            counts = status_diagnostics[row['prcstd']]
            counts['rows'] += 1
            counts['zero_volume'] += number(row['cshtrd']) == 0
            counts['missing_volume'] += number(row['cshtrd']) is None
            counts['unchanged_from_previous_supplied_row'] += n > 0 and row['prccd'] == rr[n-1]['prccd']
        metrics[-1]['status_diagnostics'] = {s: dict(c) for s, c in status_diagnostics.items()}
        for row in rr:
            if row['datadate'] in ('2006-05-15', '2006-05-16', '2011-07-01', '2011-07-04',
                                    '2022-01-28', '2022-01-31', '2022-02-01', '2026-03-16', '2026-03-17', '2026-03-18'):
                boundary_diagnostics.append({'comparison': comparison, 'gvkey': key[0], 'iid': key[1],
                    'date': row['datadate'], 'status': row['prcstd'], 'positive_close': positive(row['prccd']),
                    'positive_volume': positive(row['cshtrd']), 'mapping_count': row['mapping_count'],
                    'historical_isin': row['historical_isin'], 'candidate_screen_passes': local_candidate(row)})
            if row['mapping_count'] != '1':
                exceptions.append({'comparison': comparison, 'gvkey': key[0], 'iid': key[1],
                    'date': row['datadate'], 'positive_close': positive(row['prccd']),
                    'status': row['prcstd'], 'decision': 'QUARANTINE_NO_DATED_IDENTIFIER'})
            if not positive(row['prccd']):
                missing.append({'comparison': comparison, 'gvkey': key[0], 'iid': key[1],
                    'date': row['datadate'], 'status': row['prcstd'], 'decision': 'EXCLUDE_NO_CLOSE'})
        for left, right in zip(rr, rr[1:]):
            delta = (date.fromisoformat(right['datadate'])-date.fromisoformat(left['datadate'])).days
            if delta > 10:
                gaps.append({'comparison': comparison, 'gvkey': key[0], 'iid': key[1],
                    'last_before': left['datadate'], 'first_after': right['datadate'],
                    'calendar_days': delta, 'classification': 'UNRESOLVED_CALENDAR_SUSPENSION_OR_COVERAGE'})
            if (positive(left['ajexdi']) and positive(right['ajexdi']) and
                    left['ajexdi'] != right['ajexdi'] and positive(left['prccd']) and positive(right['prccd'])):
                factor = number(right['ajexdi']) / number(left['ajexdi'])
                raw_ratio = number(right['prccd']) / number(left['prccd'])
                adjustment.append({'comparison': comparison, 'gvkey': key[0], 'iid': key[1],
                    'before': left['datadate'], 'after': right['datadate'],
                    'factor_after_per_before': factor, 'raw_price_ratio': raw_ratio,
                    'divide_adjusted_ratio': raw_ratio/factor,
                    'multiply_adjusted_ratio': raw_ratio*factor})
    # Preserve every raw distribution row; the unique daily file is never an action source.
    distributions = []
    overlap_closes = list(read(b/'prepared/us_provider_overlap_price_comparison.csv'))
    if len(overlap_closes) != 168 or any(r['within_one_cent'] != '1' for r in overlap_closes):
        raise ValueError('Provider-overlap close control failed')
    for row in read(b/'raw/crsp_us_receipts_daily_2005_2026-09.csv'):
        if row.get('DisType') not in ('', 'N/A', 'NA', None):
            distributions.append(row)
    write(out/'corporate_action_rows.csv', distributions)
    # Raw/total-return comparisons are diagnostic only, on the same previous
    # provider date. No cross-provider return series is assembled.
    overlap_returns, overlap_summary = [], []
    for permno, ext in sorted(extensions.items()):
        diagnostics = []
        for d in sorted(set(ext) & set(us[permno])):
            current = ext[d]
            cr = us[permno][d]
            prior_date = cr['DlyPrevDt']
            if prior_date not in ext:
                continue
            prev = ext[prior_date]
            if not all(positive(r[f]) for r in (current, prev) for f in ('prccd', 'ajexdi', 'trfd')):
                continue
            price_return = (number(current['prccd'])/number(current['ajexdi'])) / (number(prev['prccd'])/number(prev['ajexdi']))-1
            total_return = (1+price_return)*number(current['trfd'])/number(prev['trfd'])-1
            record = {'permno': permno, 'date': d, 'prior_date': prior_date,
                      'compustat_price_return': price_return, 'compustat_total_return': total_return,
                      'crsp_retx': number(cr['DlyRetx']), 'crsp_ret': number(cr['DlyRet']),
                      'crsp_duration_flag': cr['DlyRetDurFlg'],
                      'ordinary_dividend': cr['DlyOrdDivAmt'], 'nonordinary_dividend': cr['DlyNonOrdDivAmt'],
                      'return_splice_approved': False}
            for name, calculated, field in [('price', price_return, 'DlyRetx'), ('total', total_return, 'DlyRet')]:
                record[name+'_absolute_difference'] = abs(calculated-number(cr[field])) if number(cr[field]) is not None else None
            diagnostics.append(record)
        overlap_returns.extend(diagnostics)
        overlap_summary.append({'permno': permno, 'comparisons': len(diagnostics),
            'max_price_return_difference': max((r['price_absolute_difference'] for r in diagnostics if r['price_absolute_difference'] is not None), default=None),
            'max_total_return_difference': max((r['total_absolute_difference'] for r in diagnostics if r['total_absolute_difference'] is not None), default=None),
            'total_differences_over_1bp': sum(r['total_absolute_difference'] is not None and r['total_absolute_difference'] > .0001 for r in diagnostics),
            'post_crsp_dates': sum(d > '2026-09-30' for d in ext),
            'splice_approved': False})
    write(out/'provider_return_overlap.csv', overlap_returns)
    # Build class-specific candidate intersections. Status/volume filters are
    # reproducible proposals; all approval fields remain false pending evidence.
    groups = defaultdict(dict)
    for row in master:
        groups[row['comparison']][row['leg']] = (row['gvkey'], row['iid'])
    samples = []
    member_rows = []

    def sample(comparison, label, keys, permno=None, start='2005-01-01', end='2026-11-06', symbol=None):
        sets = [{d for d, r in local[k].items() if start <= d <= end and local_candidate(r)} for k in keys]
        if permno:
            sets.append({d for d, r in us[permno].items() if start <= d <= min(end, '2026-09-30') and
                         us_candidate(r) and (symbol is None or same_symbol(r['TradingSymbol'], symbol))})
        dates = set.intersection(*sets)
        windows = [t for t in transitions if t['comparison'] == comparison]
        excluded = {d for d in dates if any(t['window_start_inclusive'] <= d < t['window_end_exclusive'] for t in windows)}
        dates -= excluded
        anchor = min(end, '2026-09-30') if permno else end
        horizons = []
        for years in (2, 5, 10):
            cutoff = date.fromisoformat(anchor).replace(year=date.fromisoformat(anchor).year-years).isoformat()
            horizon_dates = {d for d in dates if cutoff < d <= anchor}
            horizons.append({'years': years, 'start_exclusive': cutoff, 'end_inclusive': anchor,
                             **spans(horizon_dates), 'full_horizon_available': min(dates, default=anchor) <= cutoff,
                             'analysis_approved': False})
        identifier = comparison+'_'+label
        row = {'sample': identifier, 'comparison': comparison, 'label': label, **spans(dates),
               'excluded_asynchronous_dates': len(excluded), 'start_bound_inclusive': start,
               'end_bound_inclusive': min(end, '2026-09-30') if permno else end,
               'local_keys': [list(k) for k in keys], 'permno': permno,
               'horizons': horizons,
               'analysis_approved': False,
               'blockers': ['official_calendar_and_price_status_review', 'unexplained_gaps_and_actions_review']}
        if comparison in ('alibaba', 'hdfc', 'shell', 'novo_nordisk', 'byd', 'ping_an'):
            row['blockers'].append('point_in_time_fx_and_close_alignment')
        if permno:
            row['blockers'].append('dated_ratio_interval_certification')
        if comparison == 'shell':
            row['blockers'].append('historical_GBP_vs_GBX_scale')
        samples.append(row)
        for d in sorted(dates):
            members = {'sample': identifier, 'date': d, 'analysis_approved': 0}
            for n, k in enumerate(keys, 1):
                source = local[k][d]
                for field in ('gvkey', 'iid', 'historical_isin', 'prccd', 'curcdd', 'qunit', 'prcstd', 'cshtrd', 'ajexdi', 'trfd'):
                    members['local_'+str(n)+'_'+field] = source[field]
            if permno:
                source = us[permno][d]
                for field in ('PERMNO', 'TradingSymbol', 'DlyClose', 'DlyRet', 'DlyRetx', 'DlyPrcFlg', 'DlyRetDurFlg', 'ConditionalType'):
                    members['us_'+field] = source[field]
            member_rows.append(members)

    for comparison in ('alibaba', 'hdfc', 'novo_nordisk'):
        if len(receipts[comparison]) != 1:
            raise ValueError('Ambiguous receipt')
        sample(comparison, 'local_ADS', [groups[comparison]['local']], next(iter(receipts[comparison])))
    for comparison in ('byd', 'ping_an'):
        sample(comparison, 'A_H', [groups[comparison]['local_a'], groups[comparison]['local_h']])
    for role in ('local_pref_1', 'local_pref_2', 'local_pref_3'):
        sample('hyundai', 'common_'+role, [groups['hyundai']['local_common'], groups['hyundai'][role]])
    sample('volkswagen', 'ordinary_preferred', [groups['volkswagen']['local_common'], groups['volkswagen']['local_preferred']])
    for label, start, end in [('voting_Genussschein', '2005-01-01', '2026-03-16'),
                               ('voting_participation', '2026-03-17', '2026-11-06')]:
        sample('roche', label, [groups['roche']['local_voting'], groups['roche']['local_nonvoting']], start=start, end=end)
    shell_checks = []
    for seed in [r for r in public if r['comparison'] == 'shell' and r['leg'] == 'local']:
        keys = {k for k, values in intervals.items() if any(v['itemvalue'] == seed['public_isin_if_verified'] for v in values)}
        if len(keys) != 1:
            raise ValueError('Unresolved Shell local identity')
        key = next(iter(keys))
        symbol = 'RDS.A' if 'Class A' in seed['instrument'] else 'RDS.B' if 'Class B' in seed['instrument'] else 'SHEL'
        matching = {p for p in receipts['shell'] if any(same_symbol(r['TradingSymbol'], symbol) for r in us[p].values())}
        if len(matching) != 1:
            raise ValueError('Unresolved Shell dated receipt symbol')
        permno = next(iter(matching))
        start = seed['effective_from_if_verified']
        end = seed['effective_to_if_verified'] or '2026-11-06'
        if symbol == 'SHEL':
            start = '2022-02-01'
        sample('shell', symbol.replace('.', '_'), [key], permno, start, end, symbol)
        ratios_observed = [number(us[permno][d]['DlyClose']) / (2*number(r['prccd']))
                           for d, r in local[key].items() if start <= d <= end and d in us[permno] and
                           us_candidate(us[permno][d]) and positive(r['prccd'])]
        shell_checks.append({'class': symbol, 'common_positive_rows': len(ratios_observed),
                             'median_ADS_per_two_vendor_local_units': median(ratios_observed),
                             'scale_certified': False, 'FX_input': None})
    write(out/'proposed_sample_membership.csv', member_rows)
    write(out/'mapping_exception_decisions.csv', exceptions)
    write(out/'missing_close_decisions.csv', missing)
    write(out/'long_gaps.csv', gaps)
    write(out/'adjustment_factor_changes.csv', adjustment)
    write(out/'transition_boundary_diagnostics.csv', boundary_diagnostics)
    write(out/'reviewed_identity_intervals.csv',
          ({**r, 'review_decision': 'ACQUISITION_IDENTITY_ONLY_NO_TRADING_CERTIFICATION'}
           for values in intervals.values() for r in values))
    # Every supplied control must match and immutable packages must still verify.
    assert len(local) == 17 and sum(map(len, local.values())) == 88055
    assert len(exceptions) == 15 and len(missing) == 2
    assert sum(map(len, us.values())) == 23458
    assert len(samples) == 14
    verify_inventory(b, delivery['files'])
    verify_inventory(descriptor, descriptor_files)
    assert digest(descriptor/'manifest.json') == before_descriptor
    summary = {'receipt': {'archive_sha256': delivery['sha256'], 'zip_entries_verified': zip_count,
                'delivery_files_verified': delivery_count, 'internal_manifest_files_verified': manifest_count,
                'snapshot_reused_without_extraction': True, 'both_snapshots_unchanged': True},
               'portable_audit_controls_match': True, 'audit_output_comparison': reproduction,
               'controls': reproduced, 'local_coverage': metrics, 'long_gaps': gaps,
               'historical_identifier_rows': identifier_rows, 'overlap_closes_within_one_cent': len(overlap_closes),
               'missing_closes': missing, 'mapping_exceptions': exceptions,
               'crsp_flag_counts': {p: dict(c) for p, c in flag_counts.items()},
               'provider_return_overlap': overlap_summary, 'shell_scale_diagnostics': shell_checks,
               'adjustment_changes': len(adjustment), 'corporate_action_rows_preserved': len(distributions),
               'ratios': ratios, 'transition_windows': transitions, 'proposed_samples': samples,
               'public_review_rules': rules,
               'approved_regression_samples': 0, 'regressions_run': 0,
               'return_splicing_performed': False,
               'screen_semantics': 'PRCSTD=10, positive mapped close/unit/volume; CRSP NYSE A/RW/TR. Candidate dates only; no forward fill or calendar certification.'}
    (out/'review_summary.json').write_text(json.dumps(summary, indent=2)+'\n')
    inventory = [{'path': str(p.relative_to(out)), 'sha256': digest(p), 'size': p.stat().st_size}
                 for p in sorted(out.iterdir()) if p.is_file()]
    (out/'review_manifest.json').write_text(json.dumps({'files': inventory,
        'source_manifest_sha256': digest(b/'acquisition_manifest.json'),
        'reviewer_sha256': digest(Path(__file__)), 'python': sys.version,
        'review_rules_sha256': digest(args.rules),
        'slurm_job_id': __import__('os').environ.get('SLURM_JOB_ID')}, indent=2)+'\n')
    print(json.dumps({'receipt': summary['receipt'], 'samples': len(samples),
                      'approved': 0, 'regressions_run': 0}, indent=2))


if __name__ == '__main__':
    main()
