from pathlib import Path
import yaml

from rag.loader import load_documents
from rag.chunker import chunk_documents
from rag.retriever import get_retriever_from_config
from rag.generator import QwenGenerator
from schemas.common import Citation, RAGResponse


ANSWER_CONFIG_PATH = Path(__file__).resolve().parent.parent / "config" / "answer.yaml"


def load_yaml(path: Path):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def prepare_chunks(data_dir: str, chunk_size: int = 500, chunk_overlap: int = 100):
    docs = load_documents(data_dir)
    chunks = chunk_documents(docs, chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    return chunks


def prepare_retriever(data_dir: str, chunk_size: int = 500, chunk_overlap: int = 100):
    chunks = prepare_chunks(data_dir, chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    retriever = get_retriever_from_config()
    retriever.build_index(chunks)
    return retriever


def build_citations(retrieval_results: list[dict]) -> list[Citation]:
    citations = []
    seen = set()

    for r in retrieval_results:
        key = (r["source"], r["file_name"], r.get("page"), r["chunk_id"])
        if key in seen:
            continue
        seen.add(key)

        citations.append(
            Citation(
                source=r["source"],
                file_name=r["file_name"],
                page=r.get("page"),
                chunk_id=r["chunk_id"]
            )
        )

    return citations


def should_refuse(retrieval_results: list[dict], min_score_threshold: float) -> bool:
    if not retrieval_results:
        return True

    top_score = retrieval_results[0]["score"]
    return top_score < min_score_threshold


def answer_query(query: str, data_dir: str, top_k: int = 3) -> RAGResponse:
    answer_cfg = load_yaml(ANSWER_CONFIG_PATH)
    min_score_threshold = answer_cfg["min_score_threshold"]
    refuse_message = answer_cfg["refuse_message"]
    max_context_items = answer_cfg["max_context_items"]

    retriever = prepare_retriever(data_dir)
    results = retriever.retrieve(query, top_k=top_k)
    retrieval_results = [r.model_dump() for r in results]

    if should_refuse(retrieval_results, min_score_threshold):
        return RAGResponse(
            answer=refuse_message,
            citations=[],
            grounded=False
        )

    contexts = retrieval_results[:max_context_items]
    generator = QwenGenerator()
    answer = generator.generate(query, contexts)
    citations = build_citations(contexts)

    return RAGResponse(
        answer=answer,
        citations=citations,
        grounded=True
    )