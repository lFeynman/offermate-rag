from rag.loader import load_documents
from rag.chunker import chunk_documents


def prepare_chunks(data_dir: str, chunk_size: int = 500, chunk_overlap: int = 100):
    docs = load_documents(data_dir)
    chunks = chunk_documents(docs, chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    return chunks