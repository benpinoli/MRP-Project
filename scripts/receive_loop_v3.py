"""Verify and receive private LOOP additions without overlaying snapshots.

Run under Slurm; see BYU_ORC_AGENTS.md. ZIPs and extracted rows stay ignored.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import stat
import zipfile

from verify_loop_deliveries import digest, safe_name

ROOT = Path(__file__).resolve().parents[1]
PACKAGES = [
    ('loop_long_horizon_followup', '35a754dd094f50d611c0c95f4a5077a3aa45b43bb3917b9f3c84b950e8f8ae0a', 648953971, 273),
    ('loop_gap_closure_supplement', 'a7ad04c4143bf5a7c4b99fe712daedd45d604eead99f5ea817e07a6e5809a5dc', 267222781, 138),
]


def verify_files(root, rows):
    names = set()
    for row in rows:
        name = row['path']
        safe_name(name)
        assert name not in names
        names.add(name)
        p = root/name
        assert p.resolve().is_relative_to(root.resolve()) and not p.is_symlink()
        assert p.stat().st_size == row.get('bytes', row.get('size')), name
        assert digest(p) == row['sha256'], name


def receive(incoming, output):
    reports = []
    for name, expected, size, count in PACKAGES:
        stem = name+'_2026-11-12_v1'
        archive = incoming/(stem+'.zip')
        delivery = incoming/(stem+'.delivery.json')
        missing = [p.name for p in (archive, delivery) if not p.exists()]
        if missing:
            reports.append({'snapshot': name, 'status': 'missing', 'missing': missing})
            continue
        d = json.loads(delivery.read_text())
        assert archive.stat().st_size == d['archive_bytes'] == size
        assert digest(archive) == d['archive_sha256'] == expected
        rows = d['files']
        inventory = {r['path']: r for r in rows}
        assert len(rows) == len(inventory) == d['entry_count'] == count
        target = ROOT/'data/acquisition/2026-11-12'/name
        stage = target.with_name(name+'_receiving_'+str(os.environ.get('SLURM_JOB_ID', 'manual')))
        if target.exists():
            verify_files(target, rows)
        else:
            stage.mkdir(mode=0o700, exist_ok=False)
        with zipfile.ZipFile(archive) as z:
            infos = z.infolist()
            assert len(infos) == len(set(z.namelist())) == count
            assert set(z.namelist()) == set(inventory)
            for info in infos:
                safe_name(info.filename)
                mode = info.external_attr >> 16
                assert not info.is_dir() and not stat.S_ISLNK(mode)
                assert stat.S_IFMT(mode) in (0, stat.S_IFREG)
                row = inventory[info.filename]
                assert info.file_size == row['bytes']
            # Validate CRC and every hash while streaming with bounded memory.
            for info in infos:
                h = hashlib.sha256()
                destination = stage/info.filename
                if not target.exists():
                    destination.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
                    stream_out = destination.open('xb')
                else:
                    stream_out = None
                try:
                    with z.open(info) as stream:
                        for block in iter(lambda: stream.read(1024*1024), b''):
                            h.update(block)
                            if stream_out:
                                stream_out.write(block)
                finally:
                    if stream_out:
                        stream_out.close()
                assert h.hexdigest() == inventory[info.filename]['sha256'], info.filename
        location = target if target.exists() else stage
        internal = json.loads((location/'acquisition_manifest.json').read_text())
        verify_files(location, internal['files'])
        if not target.exists():
            stage.rename(target)
        report = {'snapshot': name, 'status': 'verified', 'archive': str(archive.relative_to(ROOT)),
                  'archive_sha256': expected, 'archive_bytes': size, 'entries_verified': count,
                  'internal_files_verified': len(internal['files']), 'delivery_sha256': digest(delivery),
                  'extracted_directory': str(target.relative_to(ROOT)), 'overlaid_existing_snapshot': False}
        reports.append(report)
        (output/'receipt_progress.json').write_text(json.dumps(reports, indent=2)+'\n')
    (output/'receipt_verification.json').write_text(json.dumps(reports, indent=2)+'\n')
    return reports


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--incoming', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    out = args.output.resolve()
    assert out.is_relative_to(ROOT/'runs')
    out.mkdir(mode=0o700, parents=True, exist_ok=False)
    (out/'executed_source.py').write_bytes(Path(__file__).read_bytes())
    from verify_loop_deliveries import verify_receipts
    # Earlier immutable deliveries and snapshot prerequisites are rechecked too.
    verify_receipts(out)
    reports = receive(args.incoming.resolve(), out)
    print(json.dumps(reports))


if __name__ == '__main__':
    main()
