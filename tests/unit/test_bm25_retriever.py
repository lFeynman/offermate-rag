from schemas.document import DocumentChunk
from rag.retriever import BM25Retriever, simple_tokenize


def test_simple_tokenize():
    text = "熟悉 Python、RAG 和 FastAPI。"
    tokens = simple_tokenize(text)

    assert "python" in tokens
    assert "rag" in tokens
    assert "fastapi" in tokens


def test_bm25_retriever_basic():
    chunks = [
        DocumentChunk(
            chunk_id="c1",
            text="岗位要求包括 Python、RAG 和 FastAPI。",
            source="data/jd/sample_jd.txt",
            file_name="sample_jd.txt",
            file_type="txt",
            page=None,
            extra_metadata={}
        ),
        DocumentChunk(
            chunk_id="c2",
            text="部署相关经验包括 Docker、Linux 和 Kubernetes。",
            source="data/tech_docs/deploy.md",
            file_name="deploy.md",
            file_type="md",
            page=None,
            extra_metadata={}
        ),
    ]

    retriever = BM25Retriever()
    retriever.build_index(chunks)

    results = retriever.retrieve("Docker 部署", top_k=1)

    assert len(results) == 1
    assert results[0].chunk_id == "c2"
    assert results[0].retrieval_type == "bm25"