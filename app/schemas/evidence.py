"""Evidence schema definitions."""

from pydantic import BaseModel, Field


class EvidenceRecord(BaseModel):
    claim_id: str
    chunk_id: str
    quote: str
    span: dict[str, int] = Field(default_factory=dict)


class ClaimRecord(BaseModel):
    claim_id: str
    claim_text: str
    status: str
    evidence: list[EvidenceRecord] = Field(default_factory=list)
