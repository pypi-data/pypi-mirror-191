from numba import njit
import numpy as np
import pandas as pd
try:
    import statsmodels.stats.api as sms
except:
    pass

def t_interval(x, alpha=0.05, alternative="two-sided"):
    return sms.DescrStatsW(x).tconfint_mean(alpha=alpha, alternative=alternative)

@njit
def compute_coverage(CI, data, stat, N, seed=0, num_iters=1000):
    low, high = CI
    estimates = resample_nb(data, stat, R=num_iters, N=N, seed=seed)[:, 0]
    return ((estimates > low) & (estimates < high)).mean()

def coverage(*args, num_N=20, **kwargs):
    Ns = np.unique(np.linspace(2, args[1].shape[0], num_N, dtype=int))
    C = np.array([compute_coverage(*args, N=N, **kwargs) for N in Ns])
    return Ns, C

def CI_specs(CIs, z, stat):
    CI_arr = CIs.values
    coverages = np.vstack([coverage(CI, z, stat)[1] for CI in CI_arr]).T
    coverages_avg = coverages[:-3].mean(axis=0)
    coverages_last = coverages[-1]
    spread = np.hstack([np.diff(CI) for CI in CI_arr])
    CIs2 = CIs.copy()
    CIs2['width'] = spread
    CIs2['coverage-last'] = coverages_last
    CIs2['coverage-3-avg'] = coverages_avg
    return CIs2

def find_best(CIs, z=None, stat=None, alpha=0.05):
    alpha_expanded_last = alpha + 0.01
    alpha_expanded_avg = alpha + 0.02
    if 'coverage-last' in CIs.columns:
        coverages_last, coverages_avg, spread = CIs[['coverage-last', 'coverage-3-avg', 'width']].values.T
    else:
        CI_arr = CIs.values
        coverages = np.vstack([coverage(CI, z, stat)[1] for CI in CI_arr]).T
        coverages_avg = coverages[:-3].mean(axis=0)
        coverages_last = coverages[-1]
        spread = np.hstack([np.diff(CI) for CI in CI_arr])
    valid = np.unique(np.hstack([np.where(coverages_last >= (1-alpha_expanded_last))[0],
                                 np.where(coverages_avg >= (1-alpha_expanded_avg))[0],
                                 np.abs(coverages_last - (1-alpha)).argmin()]))
    min_spread = spread[valid].argmin()
    return CIs.iloc[valid].iloc[min_spread]