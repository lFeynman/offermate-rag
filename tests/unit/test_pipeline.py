from rag.pipeline import prepare_chunks


def test_prepare_chunks():
    chunks = prepare_chunks("data", chunk_size=100, chunk_overlap=20)
    assert isinstance(chunks, list)
    assert len(chunks) > 0