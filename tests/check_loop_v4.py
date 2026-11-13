"""Small unit/benchmark tests; no licensed data or model fitting."""
import json
from pathlib import Path
import sys
import tempfile

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'scripts'))
from audit_loop_v3_sources import known_date
from check_loop_stability import save
from run_loop_v4 import geometric_drawdown_translation, synthetic_checks


def main():
    assert synthetic_checks() == 5
    annotated = 'unknown; availability confirmed by this announcement'
    assert annotated.startswith('unknown') and not known_date(annotated)
    assert np.isnan(geometric_drawdown_translation(np.nan))
    assert np.allclose(geometric_drawdown_translation([-100*np.log(2), 0, np.nan]),
                       [-50, 0, np.nan], equal_nan=True)
    with tempfile.TemporaryDirectory() as directory:
        path = Path(directory)/'summary.json'
        save(path, {'count': sum(np.array([True, False, True]))})
        assert json.loads(path.read_text()) == {'count': 2}
    print('Passed benchmark/unit tests, annotated unknown-date preservation, missing drawdown preservation and NumPy-count JSON logging.')


if __name__ == '__main__':
    main()
