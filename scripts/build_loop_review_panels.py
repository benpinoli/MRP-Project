"""Build private, unconverted calendar joins for interval review, not regressions."""
import argparse
import csv
import hashlib
import json
from collections import defaultdict, Counter
from pathlib import Path


def rows(path):
    with path.open(encoding='utf-8-sig', newline='') as stream:
        yield from csv.DictReader(stream)


def positive(value):
    try:
        return float(value) > 0
    except (ValueError, TypeError):
        return False


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--bundle', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--descriptor', type=Path,
                        help='Private November 11 descriptor bundle; defaults to the sibling dated snapshot')
    args = parser.parse_args()
    bundle, output = args.bundle.resolve(), args.output.resolve()
    if not output.is_relative_to(bundle.parent):
        raise ValueError('Output must remain in private acquisition storage')
    manifest = json.loads((bundle/'acquisition_manifest.json').read_text())
    for item in manifest['files']:
        path = bundle/item['path']
        if path.stat().st_size != item['size'] or hashlib.sha256(path.read_bytes()).hexdigest() != item['sha256']:
            raise ValueError('Acquisition integrity failure: '+item['path'])
    output.mkdir(exist_ok=False)
    mapping = {}
    for row in rows(bundle/'prepared/local_acquisition_identity_intervals.csv'):
        key = row['gvkey'], row['iid']
        if key in mapping and mapping[key] != row['comparison']:
            raise ValueError('Conflicting comparison mapping')
        mapping[key] = row['comparison']
    panels = defaultdict(lambda: defaultdict(dict))
    status = defaultdict(Counter)
    for row in rows(bundle/'prepared/local_requested_daily_with_dated_isin_for_review.csv'):
        key = row['gvkey'], row['iid']
        comparison = mapping[key]
        leg = 'local_'+key[0]+'_'+key[1]
        entry = panels[comparison][row['datadate']]
        if leg+'_close' in entry:
            raise ValueError('Duplicate local key/date')
        fields = {'close':'prccd','currency':'curcdd','unit':'qunit','status':'prcstd',
                  'volume':'cshtrd','adjustment':'ajexdi','return_factor':'trfd',
                  'historical_isin':'historical_isin','mapping_count':'mapping_count'}
        entry.update({leg+'_'+name:row.get(src,'') for name,src in fields.items()})
        entry[leg+'_source'] = 'Compustat_Global'
        entry[leg+'_reported_positive_mapped'] = str(int(row['prcstd']=='10' and positive(row['prccd']) and row['mapping_count']=='1'))
        status[comparison]['local_status_'+row['prcstd']] += 1
        status[comparison]['unmatched'] += row['mapping_count']!='1'
    descriptor = args.descriptor or bundle.parent.parent/'2026-11-11/wrds_descriptor_review'
    receipt_pairs = {}
    for row in rows(descriptor/'ssh_identity_review_20261112/reviewed_security_identities.csv'):
        permno = row['permno']
        if not permno:
            continue
        if permno in receipt_pairs and receipt_pairs[permno] != row['comparison']:
            raise ValueError('Conflicting private receipt mapping')
        receipt_pairs[permno] = row['comparison']
    for row in rows(bundle/'prepared/crsp_us_receipts_daily_unique_prices_and_returns_for_review.csv'):
        comparison = receipt_pairs[row['PERMNO']]
        leg = 'receipt_'+row['PERMNO']
        entry = panels[comparison][row['DlyCalDt']]
        if leg+'_close' in entry:
            raise ValueError('Duplicate CRSP daily key')
        entry.update({leg+'_close':row['DlyClose'],leg+'_return':row['DlyRet'],
                      leg+'_source':'CRSP',leg+'_symbol':row['TradingSymbol'],
                      leg+'_currency':'USD',leg+'_cusip':row['CUSIP'],
                      leg+'_venue':row['PrimaryExch'],leg+'_price_flag':row['DlyPrcFlg']})
    for row in rows(bundle/'prepared/us_receipts_compustat_extension_with_overlap_for_review.csv'):
        if row['datadate'] <= '2026-09-30':
            continue
        comparison = receipt_pairs[row['matched_crsp_permno']]
        leg = 'extension_'+row['matched_crsp_permno']
        panels[comparison][row['datadate']].update({leg+'_close':row['prccd'],leg+'_source':'Compustat_NA',
            leg+'_currency':row['curcdd'],leg+'_return':'',leg+'_status':row.get('prcstd','')})
    coverage = []
    for comparison, dates in sorted(panels.items()):
        fields = sorted({k for entry in dates.values() for k in entry})
        with (output/(comparison+'_review_panel.csv')).open('x',newline='') as stream:
            writer = csv.DictWriter(stream, fieldnames=['date','analysis_approved']+fields)
            writer.writeheader()
            for day, entry in sorted(dates.items()):
                writer.writerow({'date':day,'analysis_approved':'0',**entry})
        coverage.append({'comparison':comparison,'outer_calendar_rows':len(dates),'first':min(dates),
                         'last':max(dates),'status_counts':dict(status[comparison]),'analysis_approved':False})
    summary = {'coverage':coverage,'source_manifest_sha256':hashlib.sha256((bundle/'acquisition_manifest.json').read_bytes()).hexdigest(),
               'regressions_run':0,'conversion_or_return_splicing_performed':False,
               'corporate_actions':'Use immutable CRSP raw distribution rows and November 11 event export; unique daily file omits distribution columns.',
               'interpretation':'Outer calendar joins retain missing legs, stale/status-5 rows, mapping exceptions, Shell WI and separate provider extension. No forward fill, FX conversion or adjusted return calculation.'}
    (output/'review_summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps(summary,indent=2))


if __name__ == '__main__':
    main()
