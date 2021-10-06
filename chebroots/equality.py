from abc import ABC, abstractmethod
import math

import numpy


class EqualityChecker(ABC):
    """Abstract base class for an equality checker."""

    def __init__(self, abstol: float = 1e-16, reltol: float = 0):
        """Configure the absolute and relative tolerances"""
        self.abstol : float = abstol
        self.reltol : float = reltol

    def __call__(self, a: float, b: float) -> bool:
        """Check if two values are equal."""
        return self._isclose(a, b)

    @abstractmethod
    def _isclose(self, a: float, b: float):
        raise NotImplementedError


class EqualityCheckerMath(EqualityChecker):
    def _isclose(self, a: float, b: float) -> bool:
        return math.isclose(a, b, abs_tol=self.abstol, rel_tol=self.reltol)


class EqualityCheckerNumpy(EqualityChecker):
    def _isclose(self, a: float, b: float) -> bool:
        return numpy.isclose(a, b, atol=self.abstol, rtol=self.reltol)


class StrictEqualityChecker(EqualityCheckerMath):
    def __init__(self):
        super().__init__(abstol=0, reltol=0)
