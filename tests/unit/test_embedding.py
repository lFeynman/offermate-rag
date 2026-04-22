from schemas.document import DocumentChunk


def test_document_chunk_schema():
    chunk = DocumentChunk(
        chunk_id="c1",
        text="岗位要求包括 Python、RAG 和大模型应用经验。",
        source="data/jd/sample_jd.txt",
        file_name="sample_jd.txt",
        file_type="txt",
        page=None,
        extra_metadata={}
    )

    assert chunk.file_name == "sample_jd.txt"
    assert chunk.file_type == "txt"