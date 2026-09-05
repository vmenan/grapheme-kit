"""Core abstract contracts for grapheme-level metrics."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class BaseMetric(ABC):
    """Abstract base class for all grapheme-aware metrics."""

    @abstractmethod
    def compute(self, *args: Any, **kwargs: Any) -> Any:
        """Compute the metric score."""
        raise NotImplementedError

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        """Allow metric instance to be called directly like a function."""
        return self.compute(*args, **kwargs)


class BaseDistanceMetric(BaseMetric):
    """Abstract base class for edit distance metrics operating on graphemes."""

    @abstractmethod
    def compute(self, s1: str, s2: str) -> int | float:
        """Calculate the distance between two strings at the grapheme level."""
        raise NotImplementedError


class BaseSimilarityMetric(BaseMetric):
    """Abstract base class for similarity metrics operating on graphemes."""

    @abstractmethod
    def compute(self, s1: str, s2: str) -> float:
        """Calculate the similarity score (typically 0.0 to 1.0) between two strings."""
        raise NotImplementedError


class BaseEvaluationMetric(BaseMetric):
    """Abstract base class for NLP evaluation metrics (CER, chrF, BLEU)."""

    @abstractmethod
    def compute(self, *args: Any, **kwargs: Any) -> float:
        """Calculate the evaluation score."""
        raise NotImplementedError
