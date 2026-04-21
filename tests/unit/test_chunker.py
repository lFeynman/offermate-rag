from rag.chunker import split_text, chunk_document


def test_split_text_basic():
    text = "a" * 1000
    chunks = split_text(text, chunk_size=300, chunk_overlap=50)

    assert len(chunks) > 1
    assert all(len(chunk) <= 300 for chunk in chunks)


def test_chunk_document_txt():
    doc = {
        "text": "hello world " * 100,
        "metadata": {
            "source": "data/sample.txt",
            "file_name": "sample.txt",
            "file_type": "txt"
        }
    }

    chunks = chunk_document(doc, chunk_size=100, chunk_overlap=20)
    assert len(chunks) > 1
    assert chunks[0].file_name == "sample.txt"
    assert chunks[0].file_type == "txt"