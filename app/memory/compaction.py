"""Dual-track compaction helpers."""

from __future__ import annotations

from dataclasses import dataclass

from .evidence import Claim


@dataclass(frozen=True)
class CompactionResult:
    structured_delta: dict[str, object]
    narrative_update: str


def validate_compaction(
    *,
    claims: list[Claim],
    conflicts: dict[str, list[str]],
) -> None:
    """Validate compaction invariants for claims and conflicts."""
    for claim in claims:
        if claim.status == "verified" and not claim.evidence:
            raise ValueError("verified claims must include evidence")

    for conflict_id, citations in conflicts.items():
        if len(citations) < 2:
            raise ValueError(f"conflict {conflict_id} requires >=2 citations")


def compact(
    *,
    structured_delta: dict[str, object],
    narrative_update: str,
    claims: list[Claim],
    conflicts: dict[str, list[str]],
) -> CompactionResult:
    """Run dual-track compaction with validation."""
    validate_compaction(claims=claims, conflicts=conflicts)
    return CompactionResult(
        structured_delta=structured_delta,
        narrative_update=narrative_update,
    )
