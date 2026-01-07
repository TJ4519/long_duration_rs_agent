"""Reranking utilities with caching stub."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Iterable


class RerankLabel(str, Enum):
    DIRECT = "DIRECT"
    CONTEXT = "CONTEXT"
    NOT = "NOT"


@dataclass(frozen=True)
class RerankResult:
    candidate_id: str
    label: RerankLabel
    score: float


class RerankCache:
    """In-memory rerank cache stub."""

    def __init__(self) -> None:
        self._store: dict[str, RerankResult] = {}

    def get(self, candidate_id: str) -> RerankResult | None:
        return self._store.get(candidate_id)

    def set(self, result: RerankResult) -> None:
        self._store[result.candidate_id] = result


def rerank_candidates(
    candidate_ids: Iterable[str],
    cache: RerankCache | None = None,
    score: float = 0.5,
) -> list[RerankResult]:
    """Return stubbed rerank results for candidate IDs."""
    results: list[RerankResult] = []
    for candidate_id in candidate_ids:
        cached = cache.get(candidate_id) if cache else None
        if cached:
            results.append(cached)
            continue
        result = RerankResult(
            candidate_id=candidate_id,
            label=RerankLabel.CONTEXT,
            score=score,
        )
        if cache:
            cache.set(result)
        results.append(result)
    return results
