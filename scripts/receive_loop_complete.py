"""Verify complete private transfer and safely stage it. See BYU_ORC_AGENTS.md."""
import argparse
import hashlib
import json
from pathlib import Path
import stat
import zipfile

from verify_loop_deliveries import digest, safe_name

ROOT = Path(__file__).resolve().parents[1]
EXPECTED = '709b31f15d7935f651a37d8603143d949300f48abcf76381aa5c660d95396dc0'
EXPECTED_BYTES = 942656553


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--archive', type=Path, required=True)
    parser.add_argument('--stage', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    archive, stage, out = args.archive.resolve(), args.stage.resolve(), args.output.resolve()
    assert stage.is_relative_to(ROOT/'data/acquisition') and out.is_relative_to(ROOT/'runs')
    assert archive.stat().st_size == EXPECTED_BYTES and digest(archive) == EXPECTED
    delivery_path = archive.with_suffix('.delivery.json')
    d = json.loads(delivery_path.read_text())
    assert d['archive_sha256'] == EXPECTED and d['archive_bytes'] == EXPECTED_BYTES
    inventory = {r['path']: r for r in d['files']}
    assert len(inventory) == len(d['files']) == d['entry_count'] == 66
    stage.mkdir(mode=0o700, parents=True, exist_ok=False)
    out.mkdir(mode=0o700, parents=True, exist_ok=False)
    (out/'executed_source.py').write_bytes(Path(__file__).read_bytes())
    with zipfile.ZipFile(archive) as z:
        assert len(set(z.namelist())) == len(z.namelist()) == 66
        assert set(z.namelist()) == set(inventory)
        for info in z.infolist():
            safe_name(info.filename)
            mode = info.external_attr >> 16
            assert not info.is_dir() and not stat.S_ISLNK(mode)
            assert stat.S_IFMT(mode) in (0, stat.S_IFREG)
            assert info.file_size == inventory[info.filename]['bytes']
        for info in z.infolist():
            target = stage/info.filename
            target.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
            h = hashlib.sha256()
            with z.open(info) as source, target.open('xb') as destination:
                for block in iter(lambda: source.read(1024*1024), b''):
                    destination.write(block)
                    h.update(block)
            assert h.hexdigest() == inventory[info.filename]['sha256'], info.filename
    report = {'status': 'outer_verified_and_staged', 'archive': str(archive.relative_to(ROOT)),
        'archive_bytes': EXPECTED_BYTES, 'archive_sha256': EXPECTED, 'entries_verified': 66,
        'delivery_sha256': digest(delivery_path), 'stage': str(stage.relative_to(ROOT)),
        'flattened_paths': False, 'installer_sha256': digest(stage/'verify_install.py')}
    (out/'outer_receipt.json').write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps(report))


if __name__ == '__main__':
    main()
