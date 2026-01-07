from app.compiler import RerankCache, RerankLabel, rerank_candidates


def test_rerank_candidates_uses_cache() -> None:
    cache = RerankCache()
    first = rerank_candidates(["a"], cache=cache, score=0.7)
    second = rerank_candidates(["a"], cache=cache, score=0.2)

    assert first[0].score == 0.7
    assert second[0].score == 0.7
    assert second[0].label == RerankLabel.CONTEXT


def test_rerank_candidates_multiple_ids() -> None:
    results = rerank_candidates(["a", "b"], score=0.9)

    assert [result.candidate_id for result in results] == ["a", "b"]
    assert all(result.score == 0.9 for result in results)
