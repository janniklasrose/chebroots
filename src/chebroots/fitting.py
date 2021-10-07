import warnings

import numpy as np
from chebpy import chebfun
from chebpy.core.chebfun import Chebfun
from chebpy.core.settings import userPrefs as ChebpyPrefs


class Chebyshev:
    """Fitting a function using Chebyshev polynomials."""
    warn: bool = True
    n_fallback: int = 1000

    def __init__(self, fn) -> None:
        self.fn = fn

    def find_extrema(self, a: float, b: float) -> list[float]:
        """Find the extrema of the function in the given interval."""
        cheb = converged_chebfun(self.fn, a, b)
        dcheb = cheb.diff()
        extrema: np.ndarray = dcheb.roots()
        # In case the results are not already sorted
        extrema = np.sort(extrema)
        # Numerical error may put extrema just outside the interval
        extrema = np.clip(extrema, a, b)
        return extrema.tolist()


def converged_chebfun(fn, a: float, b: float) -> Chebfun:
    """Make a converged Chebyshev approximation."""
    cheb = chebfun(fn, [a, b], n=None)  # automatically constructed
    if not is_converged(cheb):
        n = Chebyshev.n_fallback
        if Chebyshev.warn:
            warnings.warn((
                f'Interpolation with chebfun in the interval [{a:g}, {b:g}]'
                f' failed to converge when using the automatic constructor.'
                f' Approximating using a fixed number of points ({n:d}).'
            ))
        cheb = chebfun(fn, [a, b], n=n)  # hopefully this is accurate enough
    return cheb


def is_converged(cheb: Chebfun) -> bool:
    """Check if a Chebyshev approximation is converged."""
    maxpow2 = ChebpyPrefs.maxpow2
    max_n = 2**(maxpow2-1)  # one exponent less to be safe
    return all([f.size < max_n for f in cheb.funs])