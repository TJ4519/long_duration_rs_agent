"""Context manifest builder."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Sequence


@dataclass(frozen=True)
class ContextManifest:
    run_id: str
    step_id: int
    snapshot_id: str | None
    intent: dict[str, object]
    retrieval_query: str
    candidate_chunk_ids: list[str]
    selected_chunk_ids: list[str]
    reranker_model: str
    reranker_version: str
    token_budget: dict[str, int]
    compiler_version: str


def build_context_manifest(
    *,
    run_id: str,
    step_id: int,
    snapshot_id: str | None,
    intent: dict[str, object],
    retrieval_query: str,
    candidate_chunk_ids: Sequence[str],
    selected_chunk_ids: Sequence[str],
    reranker_model: str,
    reranker_version: str,
    token_budget: dict[str, int],
    compiler_version: str,
) -> dict[str, object]:
    """Build a context manifest payload."""
    manifest = ContextManifest(
        run_id=run_id,
        step_id=step_id,
        snapshot_id=snapshot_id,
        intent=intent,
        retrieval_query=retrieval_query,
        candidate_chunk_ids=list(candidate_chunk_ids),
        selected_chunk_ids=list(selected_chunk_ids),
        reranker_model=reranker_model,
        reranker_version=reranker_version,
        token_budget=token_budget,
        compiler_version=compiler_version,
    )
    return asdict(manifest)
