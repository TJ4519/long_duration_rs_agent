"""Embedding CRUD helpers."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class EmbeddingRecord:
    chunk_id: str
    vector: list[float]


def serialize_embedding(record: EmbeddingRecord) -> dict[str, object]:
    """Serialize an embedding record for parameterized SQL inserts."""
    return {
        "chunk_id": record.chunk_id,
        "vector": record.vector,
    }


def parse_embedding(row: dict[str, object]) -> EmbeddingRecord:
    """Parse a database row into an embedding record."""
    return EmbeddingRecord(
        chunk_id=str(row["chunk_id"]),
        vector=list(row["vector"]),
    )
