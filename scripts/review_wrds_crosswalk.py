"""Verify an authorized local WRDS bundle and review identities without publishing rows.

This performs no network calls, price acquisition, or regression execution.
Identity acceptance is distinct from approval of full historical panels.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import re
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath


def relative_path(value: str) -> Path:
    normalized = value.replace('\\', '/')
    parts = PurePosixPath(normalized)
    if parts.is_absolute() or '..' in parts.parts or re.match(r'^[A-Za-z]:', normalized):
        raise ValueError(f'Unsafe manifest path: {value}')
    return Path(*parts.parts)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding='utf-8-sig', newline='') as stream:
        return list(csv.DictReader(stream))


def unique_index(rows, keys, label):
    result = {}
    for row in rows:
        key = tuple(row[k] for k in keys)
        if key in result:
            raise ValueError(f'Duplicate key in {label}')
        result[key] = row
    return result


def verify_manifest(bundle: Path) -> dict:
    manifest = json.loads((bundle/'manifest.json').read_text(encoding='utf-8'))
    for item in manifest['files']:
        path = bundle/relative_path(item['path'])
        if digest(path) != item['sha256']:
            raise ValueError(f'Hash mismatch: {item["path"]}')
        if 'rows' in item and len(read_csv(path)) != item['rows']:
            raise ValueError(f'Row count mismatch: {item["path"]}')
    for item in manifest['raw_exports']:
        path = bundle/relative_path(item['organized_file'])
        if digest(path) != item['sha256'] or len(read_csv(path)) != item['verified_rows']:
            raise ValueError('Raw export differs from acquisition manifest')
    return manifest


def review_local(candidate, master, metadata, exchanges):
    """Accept an exact current identity, never its unobserved historical continuity."""
    if not candidate['gvkey'] or not candidate['iid']:
        return 'UNRESOLVED_HISTORICAL_LOCAL_ID', 'No exact current-master assignment; do not guess IID.'
    key = (candidate['gvkey'], candidate['iid'])
    row = master.get(key)
    if row is None or row['isin'] != candidate['public_isin_seed']:
        return 'REJECTED_IDENTIFIER_MISMATCH', 'Master and public ISIN differ.'
    venue_patterns = {
        'Hong Kong Stock Exchange':r'Hong Kong', 'National Stock Exchange of India':r'National Stock Exchange of India',
        'London Stock Exchange':r'^London Stock Exchange$', 'Nasdaq Copenhagen':r'Copenhagen',
        'Shenzhen Stock Exchange':r'^Shenzhen', 'Shanghai Stock Exchange':r'^Shanghai',
        'Korea Exchange':r'^Korea Exchange', 'SIX Swiss Exchange':r'^Swiss Exchange$', 'Xetra':r'^XETRA$',
    }
    pattern = venue_patterns.get(candidate['requested_venue'])
    if not pattern or not re.search(pattern, exchanges.get(row['exchg'], ''), re.I):
        return 'REJECTED_VENUE_MISMATCH', 'Master exchange does not identify the requested local venue.'
    description = row['dsci'].upper()
    instrument = candidate['requested_instrument'].lower()
    if ('preferred' in instrument or 'preference' in instrument) and 'PFD' not in description:
        return 'REJECTED_CLASS_MISMATCH', 'Expected a preferred security.'
    if ('ordinary' in instrument or instrument in ('common','equity shares','bearer shares')) and 'ORD' not in description:
        return 'REJECTED_CLASS_MISMATCH', 'Expected an ordinary/common security.'
    meta = metadata.get(key)
    if meta:
        if meta['curcdd'] != candidate['requested_currency']:
            return 'REJECTED_CURRENCY_MISMATCH', 'Snapshot currency differs from requested local quote currency.'
        unit = float(meta['qunit'])
        if not math.isfinite(unit) or unit <= 0:
            return 'REJECTED_QUOTE_UNIT', 'Quotation unit is invalid.'
        return 'CURRENT_LOCAL_IDENTITY_ACCEPTED', 'Exact ISIN/class/venue; currency and unit observed only on snapshot date. Historical interval remains unapproved.'
    if row['secstat']=='I' and row['dldtei']:
        return 'INACTIVE_LOCAL_IDENTITY_ACCEPTED', 'Exact inactive ISIN/class/venue; historical quote currency and scale still require evidence.'
    return 'UNRESOLVED_LOCAL_METADATA', 'Exact ISIN/venue but no quote-metadata snapshot or explicit inactive status.'


def review_receipt(candidate, names):
    if not candidate['public_isin_seed']:
        return 'RATIO_BASIS_ONLY', 'Pre-subdivision share-basis record; not a separate security acquisition.'
    cusip = candidate['public_isin_seed'][2:10]
    start=max('2005-01-01',candidate.get('public_effective_from_seed') or '2005-01-01')
    end=min('2026-11-06',candidate.get('public_effective_to_seed') or '2026-11-06')
    rows = [r for r in names if r['permno']==candidate['permno'] and r['cusip']==cusip
            and r['secinfostartdt']<=end and r['secinfoenddt']>=start]
    if not rows:
        return 'REJECTED_RECEIPT_ID', 'No matching historical CUSIP and PERMNO.'
    if any(r['primaryexch']!='N' or r['sharetype']!='AD' or r['securitytype']!='EQTY' for r in rows):
        return 'REJECTED_RECEIPT_VENUE_OR_CLASS', 'Receipt family is not consistently NYSE equity depositary shares.'
    return 'US_RECEIPT_IDENTITY_ACCEPTED', 'CUSIP/PERMNO and NYSE depositary class verified; retain dated records, SHELWI, vendor cutoff and transition exclusions.'


def review_bundle(bundle: Path, output: Path) -> dict:
    bundle = bundle.resolve()
    output = output.resolve()
    # Review output must stay inside the ignored bundle, including on SSH.
    if not output.is_relative_to(bundle) or output == bundle:
        raise ValueError('Write review output to a subdirectory of the licensed bundle')
    manifest = verify_manifest(bundle)
    raw = bundle/'raw'
    master = unique_index(read_csv(raw/'compustat_global_security_master_9_issuers.csv'),('gvkey','iid'),'master')
    metadata_rows = read_csv(raw/'compustat_quote_currency_units_snapshot_2026-11-06.csv')
    if not metadata_rows or set(metadata_rows[0]) != {'gvkey','iid','curcdd','qunit','datadate'}:
        raise ValueError('Unexpected metadata columns; expected a metadata-only snapshot')
    if {r['datadate'] for r in metadata_rows} != {'2026-11-06'}:
        raise ValueError('Unexpected metadata observation dates')
    metadata = unique_index(metadata_rows,('gvkey','iid'),'snapshot')
    exchanges = {r['exchgcd']:r['exchgdesc'] for r in read_csv(raw/'compustat_exchange_code_dictionary.csv')}
    names = read_csv(raw/'crsp_us_receipt_name_history.csv')
    candidates = read_csv(bundle/'prepared/candidate_security_crosswalk_for_review.csv')
    unique_index(candidates,('candidate_row_id',),'crosswalk')
    reviewed = []
    for candidate in candidates:
        if candidate['leg']=='receipt':
            status, reason = review_receipt(candidate,names)
        else:
            status, reason = review_local(candidate,master,metadata,exchanges)
        reviewed.append({**candidate,'identity_review_status':status,'identity_review_reason':reason,
                         'full_history_approved_for_regressions':'NO',
                         'full_daily_pull_released':'NO'})
    output.mkdir(parents=True,exist_ok=True)
    table=output/'reviewed_security_identities.csv'
    with table.open('w',encoding='utf-8',newline='') as stream:
        writer=csv.DictWriter(stream,fieldnames=list(reviewed[0]))
        writer.writeheader();writer.writerows(reviewed)
    counts=Counter(r['identity_review_status'] for r in reviewed)
    summary={
        'reviewed_at_utc':datetime.now(timezone.utc).isoformat(),
        'source_manifest_sha256':digest(bundle/'manifest.json'),
        'verified_source_exports':len(manifest['raw_exports']),
        'verified_raw_rows':sum(r['verified_rows'] for r in manifest['raw_exports']),
        'reviewed_candidate_records':len(reviewed),'identity_decisions':dict(sorted(counts.items())),
        'comparisons':len({r['comparison'] for r in reviewed}),
        'full_historical_panels_approved':0,'full_daily_pull_released':False,
        'next_step':'Use accepted identities for exact scoped descriptor validation. Resolve period-specific blockers before releasing price acquisition or interpreting the nine new pair regressions. Existing validated core/Samsung/Prosus work is independent.',
        'review_table_sha256':digest(table),
    }
    (output/'review_summary.json').write_text(json.dumps(summary,indent=2)+'\n',encoding='utf-8')
    (output/'README.md').write_text(
        '# Completed identity review\n\n'
        'review_summary.json gives aggregate decisions; reviewed_security_identities.csv contains licensed row-level decisions. '
        'All original bundle hashes were verified before review. Current identity acceptance does not prove historical currency, '
        'ISIN validity, daily coverage, or regression readiness. Full daily acquisition remains held for unresolved period-specific evidence. '
        'The original acquisition manifest is immutable; this directory is a separate review layer.\n',encoding='utf-8')
    return summary


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--bundle',type=Path,required=True)
    parser.add_argument('--output',type=Path)
    args=parser.parse_args()
    result=review_bundle(args.bundle,args.output or args.bundle/'identity_review')
    print(json.dumps(result,indent=2))


if __name__=='__main__':
    main()
