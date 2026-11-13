"""Portable, read-only source checks and gated evidence integration for LOOP-LH3.

See BYU_ORC_AGENTS.md; execute in Slurm. All row-level results stay in runs/.
"""
import csv
from collections import Counter, defaultdict
from datetime import date
from decimal import Decimal
from functools import lru_cache
import json
from pathlib import Path

from verify_loop_deliveries import digest, safe_name

ROOT = Path(__file__).resolve().parents[1]


def read(path):
    with path.open(encoding='utf-8-sig', newline='') as stream:
        return list(csv.DictReader(stream))


def write(path, rows):
    fields = list(dict.fromkeys(k for r in rows for k in r))
    with path.open('w', newline='') as stream:
        writer = csv.DictWriter(stream, fields)
        writer.writeheader()
        writer.writerows(rows)


def positive(value):
    return bool(value) and Decimal(value).is_finite() and Decimal(value) > 0


def known_date(value):
    try:
        return len(value) == 10 and date.fromisoformat(value).isoformat() == value
    except (TypeError, ValueError):
        return False


@lru_cache(None)
def checked_hash(path):
    return digest(path)


def verify_reference(path, expected, snapshot=None):
    safe_name(path)
    # The follow-up fact table uses snapshot-relative source_evidence paths;
    # supplement facts and prerequisite references use repository-relative paths.
    if path.startswith('source_evidence/'):
        assert snapshot is not None
        actual = snapshot/path
    else:
        actual = ROOT/path
    assert actual.resolve().is_relative_to(ROOT/'data/acquisition')
    assert checked_hash(actual) == expected, path
    return actual.relative_to(ROOT).as_posix()


def audit_sources(cfg, out):
    old = ROOT/cfg['history_snapshot']
    supplement = ROOT/cfg['supplement_snapshot']
    receipts = json.loads((ROOT/cfg['receipt_run']/'receipt_verification.json').read_text())
    assert len(receipts) == 2 and all(r['status'] == 'verified' for r in receipts)
    # Verify exact delivered bytes at the point of use; cache source hashes.
    delivered_files = 0
    for snapshot in (old, supplement):
        internal = json.loads((snapshot/'acquisition_manifest.json').read_text())
        receipt = next(r for r in receipts if r['snapshot'] == snapshot.name)
        delivery_path = ROOT/receipt['archive']
        delivery = json.loads(delivery_path.with_suffix('.delivery.json').read_text())
        assert checked_hash(delivery_path.with_suffix('.delivery.json')) == receipt['delivery_sha256']
        for row in delivery['files']:
            safe_name(row['path'])
            p = snapshot/row['path']
            assert p.resolve().is_relative_to(snapshot) and not p.is_symlink()
            assert p.stat().st_size == row['bytes'] and checked_hash(p) == row['sha256']
            delivered_files += 1
        assert len(internal['files']) == receipt['internal_files_verified']
    refs = []
    for path in (old/'inputs/reused_source_references.json', supplement/'inputs/annual_source_references.json',
                 supplement/'prepared/prerequisite_source_references.json'):
        for row in json.loads(path.read_text()):
            verify_reference(row['path'], row['sha256'])
            refs.append(row)
    # Independently reproduce the long-history coverage counts from immutable raw.
    global_path = old/'raw/compustat_global_priority_issuers_daily_pre2005.csv'
    crsp_path = old/'raw/crsp_nvo_hdb_daily_1981_2004.csv'
    global_rows, crsp = read(global_path), read(crsp_path)
    assert len(global_rows) == 56634 and len(crsp) == 6843
    ids = read(ROOT/'data/acquisition/2026-11-12/wrds_daily_and_mapping/raw/compustat_security_identifier_history_9_issuers.csv')
    coverage = read(old/'prepared/daily_coverage_audit.csv')
    interval_decisions = []
    for row in coverage:
        if row['provider'].startswith('Compustat'):
            key = tuple(row['stable_key'].split('/'))
            rows = [r for r in global_rows if (r['gvkey'], r['iid']) == key]
            valid = [r for r in rows if positive(r['prccd'])]
            dates = [r['datadate'] for r in valid]
            all_dates = [r['datadate'] for r in rows]
            intervals = [r for r in ids if (r['gvkey'], r['iid']) == key and r['item'] == 'ISIN']
            unmapped = sum(not any(i['efffrom'] <= r['datadate'] <= i['effthru'] for i in intervals) for r in valid)
            assert unmapped == int(row['positive_rows_without_dated_isin'])
            assert Counter(r['curcdd'] for r in valid) == json.loads(row['currencies'])
            assert Counter(r['qunit'] for r in valid) == json.loads(row['quote_units'])
            assert Counter(r['prcstd'] for r in valid) == json.loads(row['price_status'])
            decision = 'held_exact_historical_quote_venue_and_other_interval_gates'
            if row['issuer'] == 'Hyundai' and row['share_class'] == 'preferred3':
                assert len(valid) == 0
                decision = 'excluded_no_positive_pre2005_price'
        else:
            rows = [r for r in crsp if r['PERMNO'] == row['stable_key'] and r['PrimaryExch'] == row['exchange']]
            valid = [r for r in rows if positive(r['DlyPrc'])]
            dates = [r['DlyCalDt'] for r in valid]
            all_dates = [r['DlyCalDt'] for r in rows]
            assert Counter(r['DlyPrcFlg'] for r in rows) == json.loads(row['price_status'])
            decision = ('excluded_Nasdaq_from_exact_NYSE_specification' if row['exchange'] != 'N'
                        else 'receipt_leg_candidate_only_no_qualified_local_extension')
        assert len(rows) == int(row['raw_rows']) and len(valid) == int(row['positive_price_rows'])
        assert min(dates, default='') == row['positive_first'] and max(dates, default='') == row['positive_last']
        assert len(all_dates)-len(set(all_dates)) == int(row['duplicate_date_excess'])
        interval_decisions.append({**row, 'v3_decision': decision, 'new_paired_interval_admitted': False,
                                   'reason': row['qualification']})
    assert len(coverage) == 13
    assert len({(r['PERMNO'], r['DlyCalDt']) for r in crsp}) == len(crsp)
    write(out/'interval_decisions.csv', interval_decisions)
    # Preserve full format/fiscal keys and descriptor-only rows in the annual join.
    annual = read(supplement/'raw/compustat_global_annual_issue_supply_1979_2025.csv')
    descriptors = read(supplement/'raw/compustat_global_annual_issue_descriptors_1979_2025.csv')
    keys = ['gvkey', 'iid', 'datadate', 'indfmt', 'datafmt', 'consol', 'popsrc', 'fyr']
    key = lambda row: tuple(row[k] for k in keys)
    assert len(annual) == 378 and len(descriptors) == 402
    index = {key(r): r for r in descriptors}
    assert len(index) == len(descriptors) and len({key(r) for r in annual}) == len(annual)
    assert all(key(r) in index for r in annual)
    assert len(set(index)-{key(r) for r in annual}) == 24
    long = read(supplement/'prepared/annual_vendor_supply_long.csv')
    assert len(long) == 1512
    reconstructed = {(key(r), field): r[field] for r in annual for field in ('cshoi', 'tstkni', 'icapi', 'pv')}
    assert len(reconstructed) == 1512
    for row in long:
        assert row['value'] == reconstructed[key(row), row['field']]
        assert row['annual_currency'] == index[key(row)]['curcdi']
        assert row['ajexi'] == index[key(row)]['ajexi']
        verify_reference(row['source_file'], row['source_sha256'])
        assert row['first_public_release_date'] == 'unknown'
    extraction = read(supplement/'prepared/annual_extraction_checks.csv')
    assert not any(r['status'] == 'FAIL' for r in extraction)
    exceptions = read(supplement/'prepared/vendor_basis_exceptions.csv')
    assert len(exceptions) == 4
    write(out/'vendor_basis_exceptions.csv', exceptions)
    # Every fact survives with provenance; none becomes a v3 price predictor.
    tables = [(old, 'dated_evidence_selected.csv', 460),
              (supplement, 'annual_structural_evidence.csv', 775),
              (supplement, 'additional_dated_structural_and_payout_evidence.csv', 53),
              (supplement, 'novo_fee_and_contract_dated_evidence.csv', 87)]
    admission, table_summaries = [], []
    passages = {r['passage_id']: r for r in json.loads((supplement/'prepared/annual_source_passages.json').read_text())}
    for snapshot, table, expected in tables:
        rows = read(snapshot/'prepared'/table)
        assert len(rows) == expected and len({r['fact_id'] for r in rows}) == expected
        for row in rows:
            for field in ('issuer', 'security_class', 'observation_date', 'effective_date',
                          'first_public_release_date', 'retrieved_at', 'field', 'value', 'unit',
                          'source_url', 'source_file', 'source_sha256', 'locator', 'vintage'):
                assert row[field].strip(), (table, row['fact_id'], field)
            resolved_source = verify_reference(row['source_file'], row['source_sha256'], snapshot)
            if row.get('source_passage_id'):
                passage = passages[row['source_passage_id']]
                assert passage['source_file'] == row['source_file']
            published = known_date(row['first_public_release_date'])
            admission.append({**row, 'v3_record_id': snapshot.name+'/'+table+'/'+row['fact_id'],
                'source_snapshot': snapshot.name, 'source_table': table, 'resolved_source_file': resolved_source,
                'publication_date_known': published, 'forecast_feature_admitted': False,
                'admission_status': 'dated_evidence_only_price_spec_has_no_structural_features' if published
                                    else 'retrospective_unknown_publication_date',
                'v3_gate': 'No backward annual propagation, report-vintage collapse, class allocation, fee-regime inference or public-float inference'})
        table_summaries.append({'table': table, 'facts': len(rows),
            'publication_date_unknown': sum(not known_date(r['first_public_release_date']) for r in rows)})
    assert len(admission) == len({r['v3_record_id'] for r in admission}) == 1375
    write(out/'evidence_admission.csv', admission)
    cash = read(supplement/'prepared/novo_final_cash_event_notices.csv')
    assert len(cash) == 6
    for row in cash:
        verify_reference(row['source_file'], row['source_sha256'])
        other = Decimal(row['USD_other']) if row['USD_other'] != 'not separately reported' else Decimal(0)
        residual = (Decimal(row['USD_gross'])-Decimal(row['USD_withholding'])-
                    Decimal(row['USD_dividend_fee'])-Decimal(row['USD_DSC'])-other-Decimal(row['USD_net']))
        assert abs(residual) <= Decimal('.000001')
        assert abs(residual-Decimal(row['USD_reconciliation_residual'])) <= Decimal('.00000001')
    march = next(r for r in cash if r['source_id'] == 'jpm_nvo_final_2021_03')
    august = next(r for r in cash if r['source_id'] == 'jpm_nvo_final_2021_08')
    assert Decimal(march['USD_dividend_fee']) == Decimal('.010')
    assert Decimal(august['USD_dividend_fee']) == Decimal('.015')
    write(out/'cash_event_checks.csv', [{**r, 'arithmetic_passed': True,
        'general_fee_effective_day': 'unknown', 'double_deduct_embedded_fx_fee': False} for r in cash])
    inventories = []
    for snapshot in (old, supplement):
        rows = read(snapshot/'prepared/source_inventory.csv')
        inventories.append({'snapshot': snapshot.name, 'source_attempt_rows': len(rows),
            'statuses': dict(Counter(r.get('download_attempt_status', r.get('status', '')) for r in rows))})
    summary = {'status': 'passed', 'delivered_files_verified_at_use': delivered_files,
        'prerequisite_references_verified': len(refs), 'raw_global_rows': len(global_rows),
        'raw_crsp_rows': len(crsp), 'coverage_rows_reproduced': len(coverage),
        'raw_distribution_rows_preserved': True, 'annual_supply_rows': len(annual),
        'annual_descriptor_rows': len(descriptors), 'annual_join_matches': 378, 'descriptor_only': 24,
        'vendor_field_observations_verified': len(long),
        'vendor_missing_field_observations': sum(r['value'] == '' for r in long),
        'fact_rows': len(admission), 'fact_tables': table_summaries, 'cash_notices_reconciled': len(cash),
        'vendor_basis_exceptions_retained': len(exceptions), 'source_inventories': inventories,
        'new_paired_intervals_released': 0, 'structural_forecast_features_admitted': 0,
        'certifies_all_transcription_values_against_original_page_layout': False,
        'scope': 'Source integrity, coverage and arithmetic; exact-venue/new-interval and feature gates retained'}
    (out/'source_audit.json').write_text(json.dumps(summary, indent=2)+'\n')
    return summary
