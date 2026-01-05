from io import BytesIO
from pathlib import Path

from app.artifacts import ArtifactManager


def test_ingest_stream_is_idempotent(tmp_path: Path) -> None:
    manager = ArtifactManager(tmp_path)
    payload = b"artifact data"

    record_a = manager.ingest_stream(BytesIO(payload), "sample.txt")
    record_b = manager.ingest_stream(BytesIO(payload), "sample.txt")

    assert record_a.content_hash == record_b.content_hash
    assert record_a.artifact_id == record_b.artifact_id
    assert record_a.byte_size == len(payload)
    assert Path(record_a.uri).exists()


def test_ingest_path_records_size(tmp_path: Path) -> None:
    manager = ArtifactManager(tmp_path)
    file_path = tmp_path / "artifact.bin"
    file_path.write_bytes(b"12345")

    record = manager.ingest_path(file_path)

    assert record.byte_size == 5
    assert Path(record.uri).exists()
