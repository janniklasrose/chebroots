from typing import Callable
import warnings

from scipy.optimize import brentq


class SingleRoot:
    """Rootfinder for a single root in an interval."""

    warn: bool = True
    abstol: float = 1e-22
    reltol: float = 1e-10
    maxiter: int = 100

    def find_root(
        self, fn: Callable[[float], float], a: float, b: float
    ) -> list[float]:
        """Find the root(s) of a function in the given interval.
        This assumes the function has one root in the open inverval (a, b).
        If one or more of the endpoints are zeros, they are returned only.
        """
        # First, check endpoints
        Fa, Fb = fn(a), fn(b)
        if Fa * Fb > 0:  # same side of x-axis and neither endpoint==0
            return []  # no root here
        if Fa == 0 or Fb == 0:  # zero(s) directly on interval boundary
            return [x for x, y in zip([a, b], [Fa, Fb]) if y == 0]

        # Now, F(a) and F(b) have different signs. Thus, there has to be a
        # single root in the interval. We are using the brentq algorithm.
        # It is very robust and fast in the case of a single root.
        # https://mathworks.com/help/matlab/ref/fzero.html
        tols = dict(xtol=self.abstol, rtol=self.reltol, maxiter=self.maxiter)
        root, result = brentq(fn, a, b, full_output=True, disp=False, **tols)
        if self.warn and not result.converged:
            warnings.warn(
                (
                    f"brentq did not converge in the interval ({a:g}, {b:g})."
                    f" Consider relaxing the tolerances ({self.abstol=}, {self.reltol=})"
                    f" or increasing the maximum number of iterations ({self.maxiter=})."
                )
            )
        return [root]
