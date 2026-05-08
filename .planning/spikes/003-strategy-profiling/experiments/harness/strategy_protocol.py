"""
Strategy protocol: the interface any recommendation strategy must implement
to be profiled by the evaluation harness.
"""

from __future__ import annotations

from typing import Protocol, runtime_checkable


@runtime_checkable
class RecommendationStrategy(Protocol):
    """Any recommendation strategy must implement this interface.

    The interface is deliberately minimal: given seed paper IDs, return
    a ranked list of (arxiv_id, score) pairs. All internal implementation
    details (which embeddings, which index, which signals) are hidden
    behind this interface.

    The protocol is runtime-checkable so the profiler can validate
    strategies before running expensive evaluations.
    """

    def recommend(
        self, seed_arxiv_ids: list[str], top_k: int = 20
    ) -> list[tuple[str, float]]:
        """Given seed paper IDs, return ranked recommendations.

        Args:
            seed_arxiv_ids: IDs of papers the user has expressed interest in.
            top_k: Number of recommendations to return.

        Returns:
            List of (arxiv_id, score) pairs, sorted by score descending.
            Scores are strategy-specific and need not be normalized.
        """
        ...

    @property
    def name(self) -> str:
        """Human-readable strategy name (e.g., 'MiniLM embedding similarity')."""
        ...

    @property
    def strategy_id(self) -> str:
        """Machine identifier matching the taxonomy (e.g., 'S1a')."""
        ...


class SimpleStrategy:
    """Convenience base class for strategies that wrap a scoring function.

    Subclass this and implement `score_all()` to return a score for every
    paper in the corpus, or use `from_score_fn()` to wrap a callable.
    """

    def __init__(
        self,
        name: str,
        strategy_id: str,
        score_fn,
        paper_ids: list[str],
    ):
        self._name = name
        self._strategy_id = strategy_id
        self._score_fn = score_fn
        self._paper_ids = paper_ids

    @property
    def name(self) -> str:
        return self._name

    @property
    def strategy_id(self) -> str:
        return self._strategy_id

    def recommend(
        self, seed_arxiv_ids: list[str], top_k: int = 20
    ) -> list[tuple[str, float]]:
        """Score all papers, exclude seeds, return top-k."""
        scores = self._score_fn(seed_arxiv_ids)
        if scores is None:
            return []

        seed_set = set(seed_arxiv_ids)
        scored = [
            (aid, float(scores[i]))
            for i, aid in enumerate(self._paper_ids)
            if aid not in seed_set
        ]
        scored.sort(key=lambda x: x[1], reverse=True)
        return scored[:top_k]


class RandomBaseline:
    """Random baseline strategy (S6a). Every strategy should beat this."""

    def __init__(self, paper_ids: list[str], seed: int = 42):
        import numpy as np

        self._paper_ids = paper_ids
        self._rng = np.random.RandomState(seed)

    @property
    def name(self) -> str:
        return "Random baseline"

    @property
    def strategy_id(self) -> str:
        return "S6a"

    def recommend(
        self, seed_arxiv_ids: list[str], top_k: int = 20
    ) -> list[tuple[str, float]]:
        seed_set = set(seed_arxiv_ids)
        candidates = [aid for aid in self._paper_ids if aid not in seed_set]
        indices = self._rng.choice(len(candidates), size=min(top_k, len(candidates)), replace=False)
        # Scores are random, decreasing so rank order is preserved
        return [
            (candidates[idx], 1.0 - i / len(indices))
            for i, idx in enumerate(indices)
        ]
