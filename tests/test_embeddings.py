from app.embeddings import EmbeddingRecord, parse_embedding, serialize_embedding


def test_serialize_embedding_round_trip() -> None:
    record = EmbeddingRecord(chunk_id="chunk-1", vector=[0.1, 0.2, 0.3])
    payload = serialize_embedding(record)

    assert payload["chunk_id"] == "chunk-1"
    assert payload["vector"] == [0.1, 0.2, 0.3]

    parsed = parse_embedding(payload)

    assert parsed == record
