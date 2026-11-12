"""Synthetic rejection/interval/integrity checks; no licensed fixtures."""
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

spec=importlib.util.spec_from_file_location('review_wrds_crosswalk',Path(__file__).resolve().parents[1]/'scripts/review_wrds_crosswalk.py')
review=importlib.util.module_from_spec(spec)
spec.loader.exec_module(review)


class CrosswalkChecks(unittest.TestCase):
    def test_receipt_ignores_old_venue_outside_requested_history(self):
        candidate={'public_isin_seed':'US1234567890','permno':'42'}
        base={'permno':'42','cusip':'12345678','primaryexch':'N','sharetype':'AD','securitytype':'EQTY',
              'secinfostartdt':'2000-01-01','secinfoenddt':'2026-09-30'}
        old={**base,'primaryexch':'Q','secinfostartdt':'1981-01-01','secinfoenddt':'1982-01-01'}
        self.assertEqual(review.review_receipt(candidate,[old,base])[0],'US_RECEIPT_IDENTITY_ACCEPTED')
        wrong={**base,'primaryexch':'Q'}
        self.assertEqual(review.review_receipt(candidate,[wrong])[0],'REJECTED_RECEIPT_VENUE_OR_CLASS')

    def test_local_isin_and_quote_currency_must_match(self):
        candidate={'gvkey':'x','iid':'y','public_isin_seed':'seed','requested_venue':'Xetra',
                   'requested_instrument':'ordinary','requested_currency':'EUR'}
        row={'isin':'seed','exchg':'e','dsci':'ORD NPV','secstat':'A','dldtei':''}
        meta={('x','y'):{'curcdd':'USD','qunit':'1'}}
        self.assertEqual(review.review_local(candidate,{('x','y'):row},meta,{'e':'XETRA'})[0],
                         'REJECTED_CURRENCY_MISMATCH')
        self.assertEqual(review.review_local(candidate,{('x','y'):{**row,'isin':'other'}},{},{'e':'XETRA'})[0],
                         'REJECTED_IDENTIFIER_MISMATCH')

    def test_unsafe_manifest_paths_rejected_and_windows_paths_portable(self):
        self.assertEqual(review.relative_path('raw\\data.csv'),Path('raw')/'data.csv')
        for path in ('../outside','/outside','C:/outside'):
            with self.assertRaises(ValueError):review.relative_path(path)

    def test_modified_source_fails_before_review(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp)
            (root/'source.csv').write_text('a\n1\n',encoding='utf-8')
            manifest={'files':[{'path':'source.csv','sha256':review.digest(root/'source.csv'),'rows':1}],
                      'raw_exports':[]}
            (root/'manifest.json').write_text(json.dumps(manifest),encoding='utf-8')
            review.verify_manifest(root)
            (root/'source.csv').write_text('a\n2\n',encoding='utf-8')
            with self.assertRaisesRegex(ValueError,'Hash mismatch'):review.verify_manifest(root)


if __name__=='__main__':unittest.main()
