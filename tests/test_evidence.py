import importlib.util

import pytest

from app.memory.evidence import Claim, Evidence, attach_evidence


def test_attach_evidence_appends() -> None:
    claim = Claim(claim_id="c1", claim_text="text", status="open", evidence=[])
    evidence = Evidence(
        claim_id="c1",
        chunk_id="chunk-1",
        quote="quote",
        span={"start": 0, "end": 4},
    )

    updated = attach_evidence(claim, evidence)

    assert len(updated.evidence) == 1
    assert updated.evidence[0].chunk_id == "chunk-1"


def test_claim_record_schema_defaults() -> None:
    if importlib.util.find_spec("pydantic") is None:
        pytest.skip("pydantic not installed")

    from app.schemas.evidence import ClaimRecord

    record = ClaimRecord(claim_id="c1", claim_text="text", status="open")

    assert record.evidence == []
