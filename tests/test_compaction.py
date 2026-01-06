import pytest

from app.memory.compaction import compact
from app.memory.evidence import Claim, Evidence


def test_compact_rejects_unverified_claims_without_evidence() -> None:
    claims = [Claim(claim_id="c1", claim_text="text", status="verified", evidence=[])]

    with pytest.raises(ValueError, match="verified claims"):
        compact(
            structured_delta={},
            narrative_update="note",
            claims=claims,
            conflicts={},
        )


def test_compact_requires_two_conflict_citations() -> None:
    claims = [
        Claim(
            claim_id="c1",
            claim_text="text",
            status="open",
            evidence=[],
        )
    ]

    with pytest.raises(ValueError, match="requires >=2 citations"):
        compact(
            structured_delta={},
            narrative_update="note",
            claims=claims,
            conflicts={"conflict-1": ["cite-1"]},
        )


def test_compact_accepts_valid_inputs() -> None:
    claims = [
        Claim(
            claim_id="c1",
            claim_text="text",
            status="verified",
            evidence=[
                Evidence(
                    claim_id="c1",
                    chunk_id="chunk-1",
                    quote="quote",
                    span={"start": 0, "end": 4},
                )
            ],
        )
    ]

    result = compact(
        structured_delta={"sources": ["s1"]},
        narrative_update="updated",
        claims=claims,
        conflicts={"conflict-1": ["cite-1", "cite-2"]},
    )

    assert result.structured_delta["sources"] == ["s1"]
    assert result.narrative_update == "updated"
