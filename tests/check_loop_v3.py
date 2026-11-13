"""Synthetic receipt extraction, admission-date and rolling-calendar checks."""
import hashlib
import json
from pathlib import Path
import stat
import sys
import tempfile
import zipfile

sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'scripts'))
import receive_loop_v3 as receiver
import audit_loop_v3_sources as sources
from audit_loop_v3_sources import known_date, positive
from run_loop_v3 import checks


def main():
    assert checks() == 5
    assert known_date('2021-11-04')
    assert not any(known_date(x) for x in ('unknown', '', '2021-13-01', '2021', 'later report'))
    assert positive('1.2') and not any(positive(x) for x in ('', '0', '-1', 'NaN'))
    with tempfile.TemporaryDirectory() as temp:
        root = Path(temp)
        snapshot = root/'data/acquisition/2026-11-12/fixture'
        path = snapshot/'source_evidence/document.txt'
        path.parent.mkdir(parents=True)
        path.write_bytes(b'synthetic citation')
        expected = hashlib.sha256(path.read_bytes()).hexdigest()
        saved_root = sources.ROOT
        sources.ROOT = root
        try:
            repository_path = path.relative_to(root).as_posix()
            assert sources.verify_reference('source_evidence/document.txt', expected, snapshot) == repository_path
            assert sources.verify_reference(repository_path, expected) == repository_path
            try:
                sources.verify_reference('../escape', expected, snapshot)
            except ValueError:
                pass
            else:
                raise AssertionError('Traversal citation accepted')
        finally:
            sources.ROOT = saved_root
    for malicious in (False, True):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            incoming, out = root/'incoming', root/'runs/output'
            incoming.mkdir(); out.mkdir(parents=True)
            (root/'data/acquisition/2026-11-12').mkdir(parents=True)
            payload = b'synthetic source only\n'
            row = {'path': 'README.md', 'bytes': len(payload), 'sha256': hashlib.sha256(payload).hexdigest()}
            manifest = json.dumps({'files': [row]}).encode()
            inventory = [row, {'path': 'acquisition_manifest.json', 'bytes': len(manifest),
                               'sha256': hashlib.sha256(manifest).hexdigest()}]
            archive = incoming/'fixture_2026-11-12_v1.zip'
            with zipfile.ZipFile(archive, 'w') as z:
                info = zipfile.ZipInfo('README.md')
                info.create_system = 3
                info.external_attr = ((stat.S_IFLNK if malicious else stat.S_IFREG) | 0o600) << 16
                z.writestr(info, payload)
                z.writestr('acquisition_manifest.json', manifest)
            checksum = receiver.digest(archive)
            d = {'archive_bytes': archive.stat().st_size, 'archive_sha256': checksum,
                 'entry_count': 2, 'files': inventory}
            archive.with_suffix('.delivery.json').write_text(json.dumps(d))
            saved_root, saved_packages = receiver.ROOT, receiver.PACKAGES
            receiver.ROOT = root
            receiver.PACKAGES = [('fixture', checksum, archive.stat().st_size, 2)]
            try:
                if malicious:
                    try:
                        receiver.receive(incoming, out)
                    except AssertionError:
                        pass
                    else:
                        raise AssertionError('Archive symlink accepted')
                    assert not (root/'data/acquisition/2026-11-12/fixture').exists()
                else:
                    assert receiver.receive(incoming, out)[0]['status'] == 'verified'
                    target = root/'data/acquisition/2026-11-12/fixture/README.md'
                    target.write_bytes(b'preserve local bytes')
                    try:
                        receiver.receive(incoming, out)
                    except AssertionError:
                        pass
                    else:
                        raise AssertionError('Differing existing snapshot overwritten')
                    assert target.read_bytes() == b'preserve local bytes'
            finally:
                receiver.ROOT, receiver.PACKAGES = saved_root, saved_packages
    print('Passed rolling-calendar boundaries, publication/price gates, safe extraction, symlink rejection and snapshot preservation.')


if __name__ == '__main__':
    main()
