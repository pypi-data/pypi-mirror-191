"""
Numba version of bias-corrected and accelerated (BCa) bootstrap.
"""
import numpy as np
import pandas as pd
from numba import njit, boolean
from itertools import product
from collections import defaultdict
import warnings
try:
    from scipy.special import ndtri, ndtr
except:
    warnings.warn('scipy not available. Numba BCa bootstrap will not work.', RuntimeWarning)
try:
    from statsmodels.nonparametric.smoothers_lowess import lowess
    from scipy.interpolate import interp1d # for interpolation of new data points
except:
    warnings.warn('scipy or statsmodels not available. Studentized bootstrap will not work.', RuntimeWarning)
try:
    shell = get_ipython().__class__.__name__
    if shell == 'ZMQInteractiveShell': # script being run in Jupyter notebook
        from tqdm.notebook import tqdm
    elif shell == 'TerminalInteractiveShell': #script being run in iPython terminal
        from tqdm import tqdm
except NameError:
    from tqdm import tqdm # Probably runing on standard python terminal.

from ..np_utils import numpy_fill 
from ._integration import simpson3oct_vec
from . import conf_interval
    
@njit
def resample_paired_nb(X, Y, func, output_len=1, R=int(1e6), seed=0):
    np.random.seed(seed)
    N = X.size    
    data_paired = np.vstack((X, Y)).T
    idxs_resampling = np.random.randint(low=0, high=N, size=R*N)
    data_resampled = data_paired[idxs_resampling].reshape(R, N, 2)    
    stat = func(X, Y)
    
    boot_sample = np.empty((R, output_len))
    for i, r in enumerate(data_resampled):
        x, y = r.T
        boot_sample[i] = func(x, y)
    return boot_sample

@njit
def resample_nb_X(X, R=int(1e5), seed=0, smooth=False, N=int(1e12)):
    """X: array of shape (N_samples, n_vars)."""
    np.random.seed(seed)
    N = min(X.shape[0], N)
    idxs_resampling = np.random.randint(low=0, high=N, size=R*N)
    data_resampled = X[idxs_resampling].reshape(R, N, X.shape[1])
    if smooth:
        def x_in_percentile(x):
            low, high  = np.percentile(x, [5, 95])
            z = x[(x>low) & (x<high)]
            return z
        def std_percentile(x):
            z = x_in_percentile(x)
            return z.std() / np.sqrt(z.size)
        h = np.array([std_percentile(x) for x in X.T])
        n_trimmed = x_in_percentile(X.T[0]).size
        for k, h_k in enumerate(h):
            data_resampled[:,:,k] += h_k * np.random.standard_t(n_trimmed, R*N)
    return data_resampled

@njit
def resample_nb(X, func, output_len=1, R=int(1e5), seed=0, smooth=False, N=int(1e12)):
    """X: array of shape (N_samples, n_vars)."""
    data_resampled = resample_nb_X(X, R=R, seed=seed, smooth=smooth, N=N)
    
    boot_sample = np.empty((R, output_len))
    for i, r in enumerate(data_resampled):
        boot_sample[i] = func(r)
    return boot_sample

@njit
def resample_block_nb(X, Y, func, output_len=1, R=int(1e5), seed=0):
    """
    X, Y:   ragged arrays or tuples. Each element is an array containing the data for a block. 
    func:   numba function f: X,Y  ->  Z,   Z: 1D array of size output_len.
    """
    np.random.seed(seed)
    def stack(arr_list):
        return np.array([a for arr in arr_list for a in arr])
    
    n_x = [len(x) for x in X]
    n_y = [len(y) for y in Y]
    idxs_resampling_x = [np.random.randint(low=0, high=n, size=R*n) for n in n_x]
    idxs_resampling_y = [np.random.randint(low=0, high=n, size=R*n) for n in n_y]
    X_resampled = [x[idxs_resampling].reshape(R, n) for x, n, idxs_resampling in zip(X, n_x, idxs_resampling_x)]
    Y_resampled = [y[idxs_resampling].reshape(R, n) for y, n, idxs_resampling in zip(Y, n_y, idxs_resampling_y)]
    
    boot_sample = np.empty((R, output_len))
    for i in range(R):
        Xi = stack([x[i] for x in X_resampled])
        Yi = stack([y[i] for y in Y_resampled])
        boot_sample[i] = func(Xi, Yi)
    return boot_sample

def resample(X, func, output_len=1, R=int(1e4), seed=0):
    """X: array of shape (N_samples, n_vars)."""
    np.random.seed(seed)
    N = X.shape[0]
    idxs_resampling = np.random.randint(low=0, high=N, size=R*N)
    data_resampled = X[idxs_resampling].reshape(R, N, X.shape[1])
    
    boot_sample = np.empty((R, output_len))
    for i, r in enumerate(data_resampled):
        boot_sample[i] = func(r)
    return boot_sample


def resample_block(X, Y, func, output_len=1, R=int(1e5), seed=0):
    """
    X, Y:   ragged arrays or tuples. Each element is an array containing the data for a block. 
    func:   numba function f: X,Y  ->  Z,   Z: 1D array of size output_len.
    """
    np.random.seed(seed)
    
    n_x = [len(x) for x in X]
    n_y = [len(y) for y in Y]
    idxs_resampling_x = [np.random.randint(low=0, high=n, size=R*n) for n in n_x]
    idxs_resampling_y = [np.random.randint(low=0, high=n, size=R*n) for n in n_y]
    X_resampled = [x[idxs_resampling].reshape(R, n) for x, n, idxs_resampling in zip(X, n_x, idxs_resampling_x)]
    Y_resampled = [y[idxs_resampling].reshape(R, n) for y, n, idxs_resampling in zip(Y, n_y, idxs_resampling_y)]
    
    boot_sample = np.empty((R, output_len))
    for i in range(R):
        Xi = np.hstack([x[i] for x in X_resampled])
        Yi = np.hstack([y[i] for y in Y_resampled])
        boot_sample[i] = func(Xi, Yi)
    return boot_sample

    
@njit
def jackknife_resampling(data):
    """Performs jackknife resampling on numpy arrays.

    Jackknife resampling is a technique to generate 'n' deterministic samples
    of size 'n-1' from a measured sample of size 'n'. The i-th
    sample  is generated by removing the i-th measurement
    of the original sample.
    """
    n = data.shape[0]
    if data.ndim > 1:
        resamples = np.empty((n, n - 1) + data.shape[1:])
        base_mask = np.ones((n), dtype=boolean)
        for i in range(n): # np.delete does not support 'axis' argument in numba.
            mask_i = base_mask.copy()
            mask_i[i] = False
            resamples[i] = data[mask_i]
    else:
        resamples = np.empty((n, n - 1))
        for i in range(n):
            resamples[i] = np.delete(data, i)
    return resamples

@njit
def jackknife_stat_nb(data, statistic):
    resamples = jackknife_resampling(data)
    stats = np.array([statistic(r) for r in resamples])
    return stats

def jackknife_stat_two_samples(data, data2, statistic):
    jk_X = jackknife_resampling(data)
    jk_Y = jackknife_resampling(data2)
    jk_XY = [*product(jk_X, jk_Y)]
    stats = np.array([statistic(*r) for r in jk_XY])
    return stats

def jackknife_stat_(data, statistic):
    resamples = jackknife_resampling(data)
    stats = np.array([statistic(r) for r in resamples])
    return stats

def _percentile_of_score(a, score, axis, account_equal=False):
    """Vectorized, simplified `scipy.stats.percentileofscore`.

    Unlike `stats.percentileofscore`, the percentile returned is a fraction
    in [0, 1].
    """
    B = a.shape[axis]
    if account_equal:
        return ((a < score).sum(axis=axis) + (a <= score).sum(axis=axis)) / (2 * B)
    else:
        return (a < score).sum(axis=axis) / B
    
def CI_bca(data, statistic, data2=None, alternative='two-sided', alpha=0.05, R=int(2e5), account_equal=False, use_numba=True, n_min=5, **kwargs):
    """If data2 is provided, assumes a block resampling and statistic takes two arguments."""
    if alternative == 'two-sided':
        probs = np.array([alpha/2, 1 - alpha/2])
    elif alternative == 'less':
        probs = np.array([0, 1-alpha])
    elif alternative == 'greater':
        probs = np.array([alpha, 1])
    else:
        raise ValueError(f"alternative '{alternative}' not valid. Available: 'two-sided', 'less', 'greater'.")
    
    if data2 is None:
        N = data.shape[0]
        if N < n_min:
            warnings.warn(f"N={N} < n_min={n_min}. Avoiding computation (returning NaNs) ...")
            return np.array([np.NaN, np.NaN])
        else:
            resample_func = resample_nb if use_numba else resample
            theta_hat_b = resample_func(data[:,None] if data.ndim == 1 else data,
                                        statistic, R=R, **kwargs).squeeze()
    else:
        total_N = lambda data: np.sum([d.shape[0] for d in data])
        N = min([total_N(data), total_N(data2)])
        if N < n_min:
            warnings.warn(f"N={N} < n_min={n_min}. Avoiding computation (returning NaNs) ...")
            return np.array([np.NaN, np.NaN])
        else:
            resample_func = resample_block_nb if use_numba else resample_block
            theta_hat_b = resample_func(data, data2, statistic, R=R, **kwargs).squeeze()
            data = np.hstack(data)
            data2 = np.hstack(data2)
        
    alpha_bca = _bca_interval(data, data2, statistic, probs, theta_hat_b, account_equal, use_numba)[0]
    
    if np.isnan(alpha_bca).all(): 
        warnings.warn('CI shows there is only one value. Check data.', RuntimeWarning)
        if data2 is None:
            sample_stat = statistic(data)
        else:
            sample_stat = statistic(data, data2)
        return np.array([sample_stat, sample_stat])
    elif alternative == 'two-sided':
        return  np.percentile(theta_hat_b, alpha_bca*100, axis=0)
    elif alternative == 'less':
         return np.array([-np.inf, np.percentile(theta_hat_b, alpha_bca[0]*100, axis=0)])
    elif alternative == 'greater':
        return np.array([np.percentile(theta_hat_b, alpha_bca[0]*100, axis=0), np.inf])
    
def _bca_interval(data, data2, statistic, probs, theta_hat_b, account_equal, use_numba):
    """Bias-corrected and accelerated interval."""
    # calculate z0_hat
    if data2 is None:
        theta_hat = statistic(data)
    else:
        theta_hat = statistic(data, data2)
    percentile = _percentile_of_score(theta_hat_b, theta_hat, axis=-1, account_equal=account_equal)
    z0_hat = ndtri(percentile)

    # calculate a_hat
    if data2 is None:
        jackknife_computer = jackknife_stat_nb if use_numba else jackknife_stat
        theta_hat_jk = jackknife_computer(data, statistic)  # jackknife resample
    else:
        theta_hat_jk = jackknife_stat_two_samples(data, data2, statistic)
    n = theta_hat_jk.shape[0]
    theta_hat_jk_dot = theta_hat_jk.mean(axis=0) 

    U = (n - 1) * (theta_hat_jk_dot - theta_hat_jk)
    num = (U**3).sum(axis=0) / n**3
    den = (U**2).sum(axis=0) / n**2
    a_hat = 1/6 * num / (den**(3/2))

    # calculate alpha_1, alpha_2
    def compute_alpha(p):
        z_alpha = ndtri(p)
        num = z0_hat + z_alpha
        return ndtr(z0_hat + num/(1 - a_hat*num))
    alpha_bca = compute_alpha(probs[(probs != 0) & (probs != 1)])
    if (alpha_bca > 1).any() or (alpha_bca < 0).any():
        warnings.warn('percentiles must be in [0, 1]. bca percentiles: {}\nForcing percentiles in [0,1]...'.format(alpha_bca), RuntimeWarning)
        alpha_bca = np.clip(alpha_bca, 0, 1)
    return alpha_bca, a_hat  # return a_hat for testing

def vs_transform(data, bootstrap_estimates, se_bootstrap, precision=1e-3, frac=2/3):
    """
    Variance-stabilizing transformation.
    """
    n_stats = bootstrap_estimates.shape[1]
    g = np.empty((data.shape[0], n_stats))
    lowess_linear_interp = []
    for i, (b, se, d) in enumerate(zip(bootstrap_estimates.T,  se_bootstrap.T, data.T)):
        x, y = lowess(se, b, frac=frac).T
        f_linear = interp1d(x, y=y, bounds_error=False, kind='linear', fill_value='extrapolate')
        z_min = d.min()
        for k, z in enumerate(tqdm(d)):
            g[k, i] = simpson3oct_vec(vs_integrand, z_min, z, precision, f_linear)[0]
        lowess_linear_interp.append(f_linear)
    return g, lowess_linear_interp

def invert_CI(CI, z, g, frac=1/10):
    CIs = np.empty(CI.shape)
    for k, (ci, zi, gi) in enumerate(zip(CI, z.T, g.T)):
        g_l, z_l = lowess(zi, gi, frac=frac).T
        f_inv = interp1d(g_l, y=z_l, bounds_error=False, kind='linear', fill_value='extrapolate')
        g_grid = np.linspace(gi.min(), gi.max(), 1000)
        CI_inv = np.empty((2))
        for i, bound in enumerate(ci):
            closest = (np.abs(bound - g_grid)).argmin()
            CI_inv[i] = f_inv(g_grid[closest])
        CIs[k] = CI_inv
    return CIs

def compute_CI_studentized(base, results, studentized_results, alpha=0.05):
    R, output_len = results.shape
    bootstrap_estimate = results.mean(axis=0)
    errors = results - bootstrap_estimate
    std_err = np.asarray(np.sqrt(np.diag(errors.T.dot(errors) / R)))
    percentiles = 100 * np.array([[alpha, 1.0 - alpha]] * output_len)
    lower = np.empty((output_len))
    upper = np.empty((output_len))
    for i in range(output_len):
        lower[i], upper[i] = np.percentile(studentized_results[:, i], percentiles[i])
    # Basic and studentized use the lower empirical quantile to compute upper and vice versa.  
    
    lower_copy = lower + 0.0
    lower = base - upper * std_err
    upper = base - lower_copy * std_err
    CI = np.vstack((lower, upper)).T
    return CI

def vs_integrand(x, f_linear):
    """Integrand of the variance-stabilizing transformation."""
    clipped_f = np.clip(f_linear(x), 1e-8, None)
    if np.isnan(clipped_f).any():
        clipped_f = numpy_fill(clipped_f)
    return 1 / clipped_f

def cov(results, base=None, recenter=False):
    """
    reps : Number of bootstrap replications
    recenter : Whether to center the bootstrap variance estimator on the average of the bootstrap samples (True), or 
                       to center on the original sample estimate (False).
    """
    if recenter:
        errors = results - np.mean(results, 0)
    else:
        assert base is not None
        errors = results - base
    return errors.T.dot(errors) / results.shape[0]

def _bootstrap_studentized_resampling(data, stat, alpha=0.05, R=10000, studentized_reps=100, recenter=False, se_func=None, seed=0, divide_by_se=True, smooth=False):
    base = np.asarray(stat(data))
    output_len = base.size
    studentized_results = np.empty((R, output_len))
    results = np.empty((R, output_len))
    se_bootstrap = np.empty((R, output_len))
    n = data.shape[0]
    if divide_by_se:
        def get_studentized(data_r, result):
            nested_resampling = resample_nb(data_r, stat, R=studentized_reps, output_len=output_len, seed=seed, smooth=smooth)        
            std_err = np.sqrt(np.diag(cov(nested_resampling, result, recenter=recenter)))
            err = result - base
            t_result = err /std_err
            return t_result, std_err
    else:
        def get_studentized(data_r, result):
            return result - base, np.NaN
    
    data_r = resample_nb_X(data, R=R, seed=seed, smooth=smooth)
    if se_func is None:
        for i, d_r in enumerate(data_r):
            result = stat(d_r)
            t_result, std_err = get_studentized(d_r, result)
            results[i] = result
            studentized_results[i] = t_result # t = (x^ - x) / s
            se_bootstrap[i] = std_err
    else:
        for i, d_r in enumerate(data_r):
            result = stat(d_r)
            se = se_func(d_r)
            results[i] = result
            studentized_results[i] = (result - base) / se
            se_bootstrap[i] = se
    return base, results, studentized_results, se_bootstrap

def CI_studentized(data, stat, R=int(1e5), alpha=0.05, smooth=False, vs=False, frac_g=2/3, frac_invert=1/10, studentized_reps=100, **kwargs):
    base, results, studentized_results, se_bootstrap = _bootstrap_studentized_resampling(data, stat, smooth=smooth, R=R, studentized_reps=studentized_reps, **kwargs)
    if vs:
        g, lowess_flinear = vs_transform(data, results, se_bootstrap, frac=frac_g)
        base_g, results_g, studentized_results_g, _ = _bootstrap_studentized_resampling(g, stat, R=R, divide_by_se=False, smooth=False)
        CI = invert_CI(compute_CI_studentized(base_g, results_g, studentized_results_g), data, g, frac=frac_invert)
    else:
        CI = compute_CI_studentized(base, results, studentized_results)
    return CI

def CI_percentile(data, stat, R=int(1e5), alpha=0.05, smooth=False, alternative='two-sided', **kwargs):
    sample_stat = stat(data)
    if hasattr(sample_stat, "__len__"):
        output_len = len(sample_stat)
    else:
        output_len = 1
    boot_sample = resample_nb(data, stat, R=R, smooth=smooth, output_len=output_len, **kwargs)
    alpha_ptg = alpha*100
    if alternative == 'two-sided':
        CI = np.percentile(boot_sample, [alpha_ptg/2, 100 - alpha_ptg/2], axis=0).T
    elif alternative == 'less':
        CI = np.vstack((-np.inf * np.ones((output_len)), np.percentile(boot_sample, 100-alpha_ptg, axis=0))).T
    elif alternative == 'greater':
        CI = np.vstack((np.percentile(boot_sample, alpha_ptg, axis=0), np.inf * np.ones((output_len)))).T
    else:
        raise ValueError(f"alternative '{alternative}' not valid. Available: 'two-sided', 'less', 'greater'.")
    return CI

def CI_all(data, stat, R=int(1e5), alpha=0.05):
    specs = dict(percentile = (CI_percentile, {}),
                 percentile_smooth = (CI_percentile, dict(smooth=True)),
                 bca = (CI_bca, {}),
                 studentized = (CI_studentized, {}),
                 studentized_smooth = (CI_studentized, dict(smooth=True)),
                 studentized_vs = (CI_studentized, dict(vs = True)),
                 studentized_vs_smooth = (CI_studentized, dict(vs=True, smooth=True))
                )
    CIs = defaultdict(list)
    for label, (func, kws) in tqdm(specs.items()):
        CI = func(data, stat, R=R, alpha=alpha, **kws)
        CIs['CI'].append(label)
        if CI.shape[0] == 1 or CI.ndim == 1:
            CI = CI.squeeze()
            CIs['low'].append(CI[0])
            CIs['high'].append(CI[1])
        else:
            CIs['low'].append(CI[:, 0])
            CIs['high'].append(CI[:, 1])
    return conf_interval.CI_specs(pd.DataFrame(CIs).set_index('CI'), data, stat)
