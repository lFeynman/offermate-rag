from rag.loader import load_documents
from rag.chunker import chunk_documents
from rag.retriever import QwenDenseRetriever
from rag.generator import QwenGenerator


def prepare_chunks(data_dir: str, chunk_size: int = 500, chunk_overlap: int = 100):
    docs = load_documents(data_dir)
    chunks = chunk_documents(docs, chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    return chunks


def prepare_retriever(data_dir: str, chunk_size: int = 500, chunk_overlap: int = 100):
    chunks = prepare_chunks(data_dir, chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    retriever = QwenDenseRetriever()
    retriever.build_index(chunks)
    return retriever


def answer_query(query: str, data_dir: str, top_k: int = 3):
    retriever = prepare_retriever(data_dir)
    results = retriever.retrieve(query, top_k=top_k)

    generator = QwenGenerator()
    contexts = [r.model_dump() for r in results]
    answer = generator.generate(query, contexts)

    return {
        "query": query,
        "answer": answer,
        "retrieval_results": contexts
    }