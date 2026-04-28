from schemas.retrieval import RetrievalResult


def test_retrieval_result_schema():
    result = RetrievalResult(
        chunk_id="c1",
        text="测试文本",
        score=0.95,
        source="data/sample.txt",
        file_name="sample.txt",
        file_type="txt",
        page=None,
        retrieval_type="bm25"
    )

    assert result.file_name == "sample.txt"
    assert isinstance(result.score, float)
    assert result.retrieval_type == "bm25"