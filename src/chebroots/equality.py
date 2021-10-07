from abc import ABC, abstractmethod
import math


class BaseEqualityChecker(ABC):
    """Abstract base class for an equality checker."""

    def __init__(self, abstol: float = 1e-16, reltol: float = 0):
        """Set the absolute and relative tolerances of the checker.
        Exact equality is achieved with abstol=reltol=0.
        """
        self.abstol : float = abstol
        self.reltol : float = reltol

    def __call__(self, a: float, b: float) -> bool:
        """Check if two values are equal."""
        return self._isclose(a, b)

    @abstractmethod
    def _isclose(self, a: float, b: float):
        raise NotImplementedError


class EqualityChecker(BaseEqualityChecker):
    """Check for equality using the built-in math module."""
    def _isclose(self, a: float, b: float) -> bool:
        return math.isclose(a, b, abs_tol=self.abstol, rel_tol=self.reltol)
