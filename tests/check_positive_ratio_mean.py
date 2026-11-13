"""Synthetic mean-objective, support and benchmark checks; no licensed rows."""
from pathlib import Path
import sys

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'scripts'))
from positive_ratio_mean import fit_ratio_mean, predict_ratio


def main():
    x = np.exp(np.linspace(-1., 1., 80))
    y = np.exp(.1+.6*np.log(x))
    fit = fit_ratio_mean(x, y)
    assert np.allclose([fit['log_intercept'], fit['log_ratio_slope']], [.1, .6], atol=1e-10)
    assert np.isclose(predict_ratio(fit, .7), np.exp(.1+.6*np.log(.7)), atol=1e-12)
    constant = fit_ratio_mean(x, np.repeat(1.2, len(x)))
    assert abs(constant['log_ratio_slope']) < 1e-10
    assert np.isclose(predict_ratio(constant, 5.), 1.2)
    # Intercept-only ratio mean is the arithmetic terminal-q mean, not mean change.
    q, qt = 100*(1-x), 100*(1-y)
    origin_q = 20.
    assert np.isclose(100*(1-y.mean())-origin_q, qt.mean()-origin_q)
    assert not np.isclose(qt.mean()-origin_q, (qt-q).mean())
    # Changing ratio units rescales the conditional mean, preserving its fit.
    scaled = fit_ratio_mean(x*10, y*10)
    assert np.isclose(predict_ratio(scaled, 7.), 10*predict_ratio(fit, .7), atol=1e-10)
    assert predict_ratio(fit, 1e-5) > 0
    for badx, bady in [(np.zeros(5), np.ones(5)), (np.ones(5), np.ones(5)), (x, -y)]:
        try:
            fit_ratio_mean(badx, bady)
        except ValueError:
            pass
        else:
            raise AssertionError('Invalid training ratios accepted')
    print('Passed exact power-mean recovery, constant terminal anchor, original-scale benchmark identity, unit equivariance, support and invalid-input rejection.')


if __name__ == '__main__':
    main()
