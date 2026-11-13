"""Small synthetic receipt safety and fixed-penalty checks; no licensed data."""
import hashlib
import json
from pathlib import Path
import sys
import tempfile
import zipfile

sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'scripts'))
import verify_loop_deliveries as delivery
from check_loop_stability import synthetic_checks


def main():
    assert synthetic_checks() == 5
    for name in ('/absolute', '../escape', 'a/../escape', 'C:/drive', 'a\\file', './file', 'a//file'):
        try:
            delivery.safe_name(name)
        except ValueError:
            pass
        else:
            raise AssertionError(name)
    assert str(delivery.safe_name('raw/leg.csv')) == 'raw/leg.csv'
    with tempfile.TemporaryDirectory() as temp:
        root = Path(temp)
        parent = root/'data/acquisition/day'
        snapshot = parent/'fixture'
        snapshot.mkdir(parents=True)
        payload = b'synthetic source only\n'
        row = {'path': 'README.md', 'size': len(payload), 'sha256': hashlib.sha256(payload).hexdigest()}
        (snapshot/'README.md').write_bytes(payload)
        (snapshot/'acquisition_manifest.json').write_text(json.dumps({'files': [row]}))
        inventory = [row, {'path': 'acquisition_manifest.json',
                         'size': (snapshot/'acquisition_manifest.json').stat().st_size,
                         'sha256': delivery.digest(snapshot/'acquisition_manifest.json')}]
        archive = parent/'fixture.zip'
        with zipfile.ZipFile(archive, 'w') as z:
            for r in inventory:
                z.write(snapshot/r['path'], r['path'])
        receipt = {'sha256': delivery.digest(archive), 'size': archive.stat().st_size, 'files': inventory}
        (parent/'fixture.delivery.json').write_text(json.dumps(receipt))
        saved_root, saved_receipts = delivery.ROOT, delivery.RECEIPTS
        try:
            delivery.ROOT = root
            delivery.RECEIPTS = [('day', 'fixture', 'fixture', receipt['sha256']),
                                 ('day', 'absent', 'absent', 'unused')]
            out = root/'out'
            out.mkdir()
            reports = delivery.verify_receipts(out)
            assert reports[0]['status'] == 'verified' and len(reports[1]['missing']) == 2
            (snapshot/'README.md').write_bytes(b'changed source bytes\n')
            try:
                delivery.verify_receipts(out)
            except AssertionError:
                pass
            else:
                raise AssertionError('Changed snapshot accepted')
        finally:
            delivery.ROOT, delivery.RECEIPTS = saved_root, saved_receipts
    print('Passed: five numerical/chronology checks, unsafe path checks, complete receipt, missing receipt, changed snapshot rejection.')


if __name__ == '__main__':
    main()
