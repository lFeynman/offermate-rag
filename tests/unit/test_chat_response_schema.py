from schemas.common import Citation, RAGResponse


def test_rag_response_schema():
    c = Citation(
        source="data/jd/sample_jd.txt",
        file_name="sample_jd.txt",
        page=None,
        chunk_id="c1"
    )

    resp = RAGResponse(
        answer="这是一个测试回答",
        citations=[c],
        grounded=True
    )

    assert resp.grounded is True
    assert len(resp.citations) == 1
    assert resp.citations[0].file_name == "sample_jd.txt"