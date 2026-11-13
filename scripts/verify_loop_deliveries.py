"""Verify private LOOP receipts without modifying snapshots. See BYU_ORC_AGENTS.md."""
import hashlib
import json
from pathlib import Path, PurePosixPath
import stat
import zipfile

ROOT = Path(__file__).resolve().parents[1]
RECEIPTS = [
    ('2026-11-11', 'wrds_descriptor_review', 'wrds_descriptor_review_2026-11-11',
     'd8ab4624c9536d9d8789e091886f43b3de8b83bf436d98f50c8412289e4b1748'),
    ('2026-11-12', 'wrds_daily_and_mapping', 'wrds_daily_and_mapping_2026-11-12',
     'a65bfef416b82720c6c8200a64905e6d8fbfdb08d1515d8225ee955cd681bf97'),
    ('2026-11-12', 'loop_long_horizon_followup', 'loop_long_horizon_followup_2026-11-12_v1',
     '35a754dd094f50d611c0c95f4a5077a3aa45b43bb3917b9f3c84b950e8f8ae0a'),
]


def digest(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def safe_name(name):
    p = PurePosixPath(name)
    if (not name or '\\' in name or ':' in name or p.is_absolute()
            or any(s in ('', '.', '..') for s in name.split('/'))):
        raise ValueError('Unsafe archive/inventory path')
    return p


def verify_receipts(out):
    reports = []
    for day, directory, stem, expected in RECEIPTS:
        parent = ROOT/'data/acquisition'/day
        archive, delivery = parent/(stem+'.zip'), parent/(stem+'.delivery.json')
        report = {'snapshot': directory, 'archive': str(archive.relative_to(ROOT)),
                  'missing': [p.name for p in (archive, delivery) if not p.exists()]}
        if report['missing']:
            report['status'] = 'missing_not_qualified'
            reports.append(report)
            continue
        d = json.loads(delivery.read_text())
        assert digest(archive) == expected == d.get('archive_sha256', d.get('sha256'))
        assert archive.stat().st_size == d.get('archive_bytes', d.get('size'))
        inventory = {r['path']: r for r in d['files']}
        assert len(inventory) == len(d['files'])
        if directory == 'loop_long_horizon_followup':
            assert archive.stat().st_size == 648953971 and len(inventory) == 273
        for name in inventory:
            safe_name(name)
        with zipfile.ZipFile(archive) as z:
            names = z.namelist()
            assert len(names) == len(set(names)) and set(names) == set(inventory)
            for info in z.infolist():
                safe_name(info.filename)
                mode = info.external_attr >> 16
                assert not stat.S_ISLNK(mode) and not info.is_dir()
                assert stat.S_IFMT(mode) in (0, stat.S_IFREG)
                row = inventory[info.filename]
                assert info.file_size == row.get('bytes', row.get('size'))
                with z.open(info) as stream:
                    assert hashlib.file_digest(stream, 'sha256').hexdigest() == row['sha256']
        snapshot = parent/directory
        for name, row in inventory.items():
            p = snapshot/name
            assert p.resolve().is_relative_to(snapshot.resolve()) and not p.is_symlink()
            assert p.stat().st_size == row.get('bytes', row.get('size'))
            assert digest(p) == row['sha256'], name
        internal = snapshot/('manifest.json' if directory == 'wrds_descriptor_review' else 'acquisition_manifest.json')
        manifest = json.loads(internal.read_text())
        for row in manifest['files']:
            # The immutable November 11 manifest was generated on Windows.
            # Only its internal references may use separators from Windows;
            # ZIP entries and the delivery inventory remain strict POSIX paths.
            name = row['path'].replace('\\', '/') if directory == 'wrds_descriptor_review' else row['path']
            safe_name(name)
            p = snapshot/name
            assert p.resolve().is_relative_to(snapshot.resolve()) and not p.is_symlink()
            assert p.stat().st_size == row.get('bytes', row.get('size'))
            assert digest(p) == row['sha256'], row['path']
        report.update(status='verified', archive_sha256=expected, archive_bytes=archive.stat().st_size,
                      delivery_sha256=digest(delivery), entries_verified=len(inventory),
                      internal_files_verified=len(manifest['files']), snapshot_unchanged=True,
                      remote_agent_handoff_present=(snapshot/'REMOTE_AGENT_HANDOFF.md').exists(),
                      private_handoff='SSH_AGENT_PROMPT.md' if (snapshot/'SSH_AGENT_PROMPT.md').exists() else None)
        reports.append(report)
    (out/'delivery_verification.json').write_text(json.dumps(reports, indent=2)+'\n')
    return reports
