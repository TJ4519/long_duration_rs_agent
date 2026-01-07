"""Artifact ingestion and storage."""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
from pathlib import Path
import shutil
from typing import BinaryIO
import uuid


@dataclass(frozen=True)
class ArtifactRecord:
    artifact_id: str
    uri: str
    content_hash: str
    byte_size: int


class ArtifactManager:
    """Store artifacts by content hash with pointer-only metadata."""

    def __init__(self, storage_dir: Path) -> None:
        self._storage_dir = storage_dir
        self._storage_dir.mkdir(parents=True, exist_ok=True)

    def ingest_stream(self, stream: BinaryIO, filename: str) -> ArtifactRecord:
        """Ingest a stream, storing by content hash with idempotency."""
        temp_path = self._storage_dir / f".{filename}.upload"
        hasher = hashlib.sha256()
        byte_size = 0

        with temp_path.open("wb") as handle:
            while True:
                chunk = stream.read(8192)
                if not chunk:
                    break
                handle.write(chunk)
                hasher.update(chunk)
                byte_size += len(chunk)

        content_hash = hasher.hexdigest()
        final_path = self._storage_dir / content_hash

        if final_path.exists():
            temp_path.unlink(missing_ok=True)
        else:
            shutil.move(str(temp_path), str(final_path))

        artifact_id = str(uuid.uuid5(uuid.NAMESPACE_URL, content_hash))
        return ArtifactRecord(
            artifact_id=artifact_id,
            uri=str(final_path),
            content_hash=content_hash,
            byte_size=byte_size,
        )

    def ingest_path(self, path: Path) -> ArtifactRecord:
        """Ingest a local file path."""
        with path.open("rb") as handle:
            return self.ingest_stream(handle, path.name)
