from typing import Callable, Optional, Tuple

from .fitting import Chebyshev
from .rootfinding import SingleRoot
from .equality import EqualityChecker


class ChebRoots:
    """Recursive rootfinder using Chebyshev approximation."""

    def __init__(self, fn: Callable) -> None:
        self.fn = fn
        self.cheb = Chebyshev(fn)
        self._singleroot = SingleRoot()
        self._equality_checker = EqualityChecker()
        self._strict_equality_checker = EqualityChecker(0, 0)

    def find_all_roots(
        self, interval: list[float]
    ) -> Tuple[list[float], Optional[list[float]]]:
        """Find all roots in the given interval.
        The output is a tuple of:
          - the roots x0 where F(x0) := 0, and
          - the values of F(x0), which correspond to the numerical error
        """

        # Subdivide the function into segments of at most one root
        intervals = self._subdivide(interval)  # update intervals

        # Find the local root in each interval
        roots_all: list[float] = []
        for a, b in intervals:
            root = self._singleroot.find_root(self.fn, a, b)
            # Due to end points potentially being roots, each interval may
            # contain more than one root. Thus, `extend` is needed.
            roots_all.extend(root)

        # Post-process
        x0 = sorted(set(roots_all))  # ensure roots are sorted and unique
        if len(x0) > 0:
            error = self.fn(x0)  # this is the error since F(x0) := 0
        else:
            error = None
        return x0, error

    def _subdivide(self, breakpoints: list[float]) -> list[Tuple[float, float]]:
        """Recursively split fn at the breakpoints into intervals with at most one root."""
        new_breakpoints: list[Tuple[float, float]] = []
        for x_L, x_R in zip(breakpoints[:-1], breakpoints[1:]):
            extrema = self.find_local_extrema(x_L, x_R)
            if extrema == [x_L, x_R]:  # same interval came out as we put in
                breakpoints_i = [tuple(extrema)]  # exit condition
            else:
                breakpoints_i = self._subdivide(extrema)  # recurse
            new_breakpoints.extend(breakpoints_i)
        return new_breakpoints

    def find_local_extrema(self, x_L: float, x_R: float) -> list[float]:
        """Find local extrema, including endpoints."""

        # Check that the interval is not degenerate
        if self._strict_equality_checker(x_L, x_R):
            return [x_L, x_R]

        # Add end points
        if extrema := self.cheb.find_extrema(x_L, x_R):  # at least one extremum found
            # endpoint a
            if self._equality_checker(extrema[0], x_L):
                extrema[0] = x_L
            else:
                extrema.insert(0, x_L)
            # endpoint b
            if len(extrema) > 1 and self._equality_checker(extrema[-1], x_R):
                # size check ensures we don't override x_range[0]
                extrema[-1] = x_R
            else:
                extrema.insert(len(extrema), x_R)
        else:  # no extremum found
            extrema = [x_L, x_R]

        return extrema
