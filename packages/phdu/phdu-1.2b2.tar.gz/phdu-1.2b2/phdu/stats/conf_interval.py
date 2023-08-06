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
    np.random.seed(0)
    low, high = CI
    estimates = np.empty((num_iters))
    for i in range(num_iters):
        x_r = np.random.choice(data, size=N, replace=True)
        estimates[i] = stat(x_r)
    return ((estimates > low) & (estimates < high)).mean()

def coverage(*args, num_N=20, **kwargs):
    Ns = np.unique(np.linspace(2, args[1].shape[0], num_N, dtype=int))
    C = np.array([compute_coverage(*args, N=N, **kwargs) for N in Ns])
    return Ns, C

def find_best(CIs, z, stat, alpha=0.06):
    CI_arr = CIs.values
    coverages = np.vstack([coverage(CI, z, stat)[1] for CI in CI_arr]).T[:-3].mean(axis=0)
    spread = np.hstack([np.diff(CI) for CI in CI_arr])
    valid = np.unique(np.hstack([np.where(coverages >= (1-alpha))[0], np.abs(coverages - (1-alpha)).argmin()]))
    min_spread = spread[valid].argmin()
    return CIs.iloc[valid].iloc[min_spread]