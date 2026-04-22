from typing import List
from pathlib import Path
import yaml
import numpy as np
import os
from openai import OpenAI

from schemas.document import DocumentChunk
from schemas.retrieval import RetrievalResult


RETRIEVAL_CONFIG_PATH = Path(__file__).resolve().parent.parent / "config" / "retrieval.yaml"
MODEL_CONFIG_PATH = Path(__file__).resolve().parent.parent / "config" / "model.yaml"


def load_yaml(path: Path):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


class QwenDenseRetriever:
    def __init__(self):
        retrieval_cfg = load_yaml(RETRIEVAL_CONFIG_PATH)
        model_cfg = load_yaml(MODEL_CONFIG_PATH)

        api_key = os.getenv(model_cfg["api_key_env"])
        if not api_key:
            raise ValueError(f"环境变量 {model_cfg['api_key_env']} 未设置")

        self.client = OpenAI(
            api_key=api_key,
            base_url=model_cfg["base_url"]
        )

        self.embedding_model = retrieval_cfg["embedding_model"]
        self.embedding_dimensions = retrieval_cfg.get("embedding_dimensions", 1024)
        self.top_k = retrieval_cfg["top_k"]
        self.batch_size = retrieval_cfg.get("batch_size", 10)
        self.normalize_embeddings = retrieval_cfg.get("normalize_embeddings", True)

        self.chunks: List[DocumentChunk] = []
        self.chunk_embeddings = None

    def _normalize(self, vectors: np.ndarray) -> np.ndarray:
        norms = np.linalg.norm(vectors, axis=1, keepdims=True)
        norms[norms == 0] = 1e-12
        return vectors / norms

    def _embed_texts(self, texts: List[str]) -> np.ndarray:
        all_embeddings = []

        for i in range(0, len(texts), self.batch_size):
            batch = texts[i:i + self.batch_size]

            resp = self.client.embeddings.create(
                model=self.embedding_model,
                input=batch,
                dimensions=self.embedding_dimensions
            )

            batch_embeddings = [item.embedding for item in resp.data]
            all_embeddings.extend(batch_embeddings)

        embeddings = np.array(all_embeddings, dtype=np.float32)

        if self.normalize_embeddings:
            embeddings = self._normalize(embeddings)

        return embeddings

    def build_index(self, chunks: List[DocumentChunk]):
        self.chunks = chunks
        texts = [chunk.text for chunk in chunks]
        self.chunk_embeddings = self._embed_texts(texts)

    def retrieve(self, query: str, top_k: int = None) -> List[RetrievalResult]:
        if self.chunk_embeddings is None or len(self.chunks) == 0:
            raise ValueError("Retriever index is empty. Please call build_index first.")

        k = top_k or self.top_k

        query_embedding = self._embed_texts([query])[0]
        scores = np.dot(self.chunk_embeddings, query_embedding)

        top_indices = np.argsort(scores)[::-1][:k]

        results = []
        for idx in top_indices:
            chunk = self.chunks[idx]
            score = float(scores[idx])

            results.append(
                RetrievalResult(
                    chunk_id=chunk.chunk_id,
                    text=chunk.text,
                    score=score,
                    source=chunk.source,
                    file_name=chunk.file_name,
                    file_type=chunk.file_type,
                    page=chunk.page,
                )
            )

        return results