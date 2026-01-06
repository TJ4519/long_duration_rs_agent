"""Evidence ledger helpers."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Evidence:
    claim_id: str
    chunk_id: str
    quote: str
    span: dict[str, int]


@dataclass(frozen=True)
class Claim:
    claim_id: str
    claim_text: str
    status: str
    evidence: list[Evidence]


def attach_evidence(claim: Claim, evidence: Evidence) -> Claim:
    """Return a new claim with evidence appended."""
    return Claim(
        claim_id=claim.claim_id,
        claim_text=claim.claim_text,
        status=claim.status,
        evidence=[*claim.evidence, evidence],
    )
