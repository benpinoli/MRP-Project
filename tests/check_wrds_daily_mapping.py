"""Synthetic archive/integrity rejection checks; no licensed fixtures."""
import importlib.util
import json
import tempfile
import unittest
import zipfile
from pathlib import Path

spec = importlib.util.spec_from_file_location('daily_review', Path(__file__).resolve().parents[1]/'scripts/review_wrds_daily_mapping.py')
review = importlib.util.module_from_spec(spec)
spec.loader.exec_module(review)


class ReceiptChecks(unittest.TestCase):
    def test_paths_reject_posix_windows_and_traversal(self):
        for path in ('/outside', '../outside', 'raw/../outside', 'C:/outside', 'raw\\outside', './outside', 'raw//outside'):
            with self.assertRaises(ValueError):
                review.safe_path(path)

    def test_changed_source_and_symlink_fail(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            source = root/'data'
            source.write_bytes(b'original')
            records = [{'path': 'data', 'size': 8, 'sha256': review.digest(source)}]
            self.assertEqual(review.verify_inventory(root, records), 1)
            source.write_bytes(b'modified')
            with self.assertRaises(ValueError):
                review.verify_inventory(root, records)
            source.unlink()
            (root/'target').write_bytes(b'original')
            source.symlink_to(root/'target')
            with self.assertRaises(ValueError):
                review.verify_inventory(root, records)

    def test_zip_member_integrity_and_symlink(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            source = root/'source'
            source.write_bytes(b'original')
            archive = root/'bundle.zip'
            for link in (False, True):
                with zipfile.ZipFile(archive, 'w') as z:
                    info = zipfile.ZipInfo('raw/data')
                    if link:
                        info.create_system = 3
                        info.external_attr = 0o120777 << 16
                    z.writestr(info, b'original')
                delivery = {'size': archive.stat().st_size, 'sha256': review.digest(archive),
                            'files': [{'path': 'raw/data', 'size': 8, 'sha256': review.digest(source)}]}
                if link:
                    with self.assertRaises(ValueError):
                        review.verify_zip(archive, delivery)
                else:
                    self.assertEqual(review.verify_zip(archive, delivery), 1)
                    delivery['files'][0]['sha256'] = '0'*64
                    with self.assertRaises(ValueError):
                        review.verify_zip(archive, delivery)

    def test_shelwi_and_nontrades_do_not_enter_regular_way_sample(self):
        row = {'PrimaryExch': 'N', 'DlyPrcFlg': 'TR', 'TradingStatusFlg': 'A',
               'ConditionalType': 'RW', 'DlyClose': '20', 'DlyVol': '100'}
        self.assertTrue(review.us_candidate(row))
        for changes in ({'ConditionalType': 'WI'}, {'DlyPrcFlg': 'BA'}, {'DlyVol': '0'}, {'DlyClose': ''}, {'TradingStatusFlg': 'S'}):
            self.assertFalse(review.us_candidate({**row, **changes}))


if __name__ == '__main__':
    unittest.main()
