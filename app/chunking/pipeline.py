"""Chunking pipeline helpers."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Chunk:
    chunk_index: int
    start_offset: int
    end_offset: int
    text_preview: str


def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> list[Chunk]:
    """Split text into overlapping chunks with provenance offsets."""
    if chunk_size <= 0:
        raise ValueError("chunk_size must be positive")
    if overlap < 0:
        raise ValueError("overlap must be non-negative")
    if overlap >= chunk_size:
        raise ValueError("overlap must be smaller than chunk_size")

    chunks: list[Chunk] = []
    start = 0
    index = 0
    length = len(text)

    while start < length:
        end = min(start + chunk_size, length)
        preview = text[start:end]
        chunks.append(
            Chunk(
                chunk_index=index,
                start_offset=start,
                end_offset=end,
                text_preview=preview,
            )
        )
        if end == length:
            break
        index += 1
        start = end - overlap

    return chunks
