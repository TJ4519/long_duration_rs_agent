from app.chunking import chunk_text


def test_chunk_text_produces_overlapping_chunks() -> None:
    text = "abcdefghijklmnopqrstuvwxyz"
    chunks = chunk_text(text, chunk_size=10, overlap=2)

    assert len(chunks) == 3
    assert chunks[0].start_offset == 0
    assert chunks[0].end_offset == 10
    assert chunks[1].start_offset == 8
    assert chunks[1].end_offset == 18
    assert chunks[2].start_offset == 16
    assert chunks[2].end_offset == 26


def test_chunk_text_rejects_invalid_sizes() -> None:
    text = "abc"

    try:
        chunk_text(text, chunk_size=0)
    except ValueError as exc:
        assert "chunk_size" in str(exc)
    else:
        raise AssertionError("expected ValueError for chunk_size")

    try:
        chunk_text(text, chunk_size=5, overlap=5)
    except ValueError as exc:
        assert "overlap" in str(exc)
    else:
        raise AssertionError("expected ValueError for overlap")
