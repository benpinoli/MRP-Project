"""Positive continuous-response quasi-mean fit; see BYU_ORC_AGENTS.md.

An exponential conditional mean, not exponentiated log-OLS or a count model.
"""
import numpy as np


def fit_ratio_mean(ratio, terminal_ratio):
    x, y = np.asarray(ratio, dtype=float), np.asarray(terminal_ratio, dtype=float)
    if not (len(x) == len(y) and len(x) >= 2 and np.isfinite(x).all() and np.isfinite(y).all()
            and (x > 0).all() and (y > 0).all()):
        raise ValueError('Positive finite training ratios required')
    logx = np.log(x)
    center, scale = float(logx.mean()), float(logx.std())
    if scale <= 1e-14:
        raise ValueError('Training log-ratio is constant at numerical precision')
    z = (logx-center)/scale
    target_moment = float(np.dot(y/y.sum(), z))

    def score(beta):
        eta = beta*z
        weight = np.exp(eta-eta.max())
        return float(np.dot(weight/weight.sum(), z)-target_moment)

    lower, upper = -1., 1.
    for _ in range(30):
        if score(lower) <= 0 <= score(upper):
            break
        lower *= 2; upper *= 2
    else:
        raise ValueError('Finite profile-score root not bracketed')
    for iterations in range(1, 101):
        beta = (lower+upper)/2
        value = score(beta)
        if value > 0:
            upper = beta
        else:
            lower = beta
        if upper-lower <= 1e-13*(1+abs(beta)):
            break
    beta = (lower+upper)/2
    eta = beta*z
    maximum = float(eta.max())
    log_mean_exp = maximum+float(np.log(np.exp(eta-maximum).mean()))
    intercept = float(np.log(y.mean())-log_mean_exp)
    fitted = np.exp(intercept+beta*z)
    relative_intercept_score = float(np.mean(fitted-y)/y.mean())
    relative_slope_score = float(np.mean((fitted-y)*z)/y.mean())
    if max(abs(relative_intercept_score), abs(relative_slope_score)) > 1e-10:
        raise ValueError('Mean-score equations failed tolerance')
    return {'intercept_standardized': intercept, 'slope_standardized': float(beta),
            'log_ratio_center': center, 'log_ratio_scale': scale,
            'log_intercept': float(intercept-beta*center/scale), 'log_ratio_slope': float(beta/scale),
            'relative_intercept_score': relative_intercept_score,
            'relative_slope_score': relative_slope_score, 'bisection_iterations': iterations}


def predict_ratio(fit, ratio):
    if not np.isfinite(ratio) or ratio <= 0:
        raise ValueError('Positive finite forecast-origin ratio required')
    eta = fit['intercept_standardized']+fit['slope_standardized']*(np.log(ratio)-fit['log_ratio_center'])/fit['log_ratio_scale']
    with np.errstate(over='ignore', under='ignore', invalid='ignore'):
        prediction = float(np.exp(eta))
    if not np.isfinite(prediction) or prediction <= 0:
        raise ValueError('Forecast mean overflow/underflow or nonpositive ratio')
    return prediction
