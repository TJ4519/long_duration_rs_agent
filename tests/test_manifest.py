from app.compiler.manifest import build_context_manifest


def test_build_context_manifest_serializes_fields() -> None:
    manifest = build_context_manifest(
        run_id="run-1",
        step_id=2,
        snapshot_id=None,
        intent={"goal": "test"},
        retrieval_query="query",
        candidate_chunk_ids=["c1", "c2"],
        selected_chunk_ids=["c1"],
        reranker_model="model-a",
        reranker_version="v1",
        token_budget={"total": 1000},
        compiler_version="0.1.0",
    )

    assert manifest["run_id"] == "run-1"
    assert manifest["step_id"] == 2
    assert manifest["candidate_chunk_ids"] == ["c1", "c2"]
    assert manifest["selected_chunk_ids"] == ["c1"]
    assert manifest["token_budget"]["total"] == 1000
