from typing import List, Dict
from pathlib import Path
import yaml
import numpy as np
import os
import re
from openai import OpenAI
from rank_bm25 import BM25Okapi

from schemas.document import DocumentChunk
from schemas.retrieval import RetrievalResult


'''
RAG场景下的多模式文本检索系统，支持多种检索模式：
- Dense Retriever：基于大模型生成的文本嵌入进行语义检索，适合捕捉深层次语义关系。
- BM25 Retriever：基于词频和逆文档频率的传统检索算法，适合精确匹配和关键词检索。
- Hybrid Retriever：结合Dense和BM25的优势，通过加权融合两者的得分进行检索。
'''
RETRIEVAL_CONFIG_PATH = Path(__file__).resolve().parent.parent / "config" / "retrieval.yaml"
MODEL_CONFIG_PATH = Path(__file__).resolve().parent.parent / "config" / "model.yaml"


def load_yaml(path: Path):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def simple_tokenize(text: str) -> List[str]:
    """
    简单中英文混合 tokenizer。
    - 英文、数字、技术词按连续 token 保留
    - 中文按单字切分
    适合作为 BM25 的轻量 baseline。
    """
    text = text.lower()
    tokens = re.findall(r"[a-zA-Z0-9\+\#\.\-_]+|[\u4e00-\u9fff]", text)
    return tokens


def minmax_normalize(score_map: Dict[str, float]) -> Dict[str, float]:
    '''
    dense和bm25的分数范围不同，直接加权会导致一个过大一个过小，无法发挥两者优势。
    '''
    if not score_map:
        return {}

    values = list(score_map.values())
    min_score = min(values)
    max_score = max(values)

    if max_score == min_score:
        return {k: 1.0 for k in score_map}

    return {
        k: (v - min_score) / (max_score - min_score)
        for k, v in score_map.items()
    }


class QwenDenseRetriever:
    def __init__(self):
        # 从配置文件读取检索和模型参数，避免把模型名、维度、top_k 写死在代码里。
        retrieval_cfg = load_yaml(RETRIEVAL_CONFIG_PATH)
        model_cfg = load_yaml(MODEL_CONFIG_PATH)

        # 这里使用 DashScope 的 OpenAI 兼容接口，所以先从环境变量读取 API Key。
        api_key = os.getenv(model_cfg["api_key_env"])
        if not api_key:
            raise ValueError(f"环境变量 {model_cfg['api_key_env']} 未设置")

        # 初始化 OpenAI 客户端，后面会用它去调用 embedding 接口。
        self.client = OpenAI(
            api_key=api_key,
            base_url=model_cfg["base_url"]
        )

        # 这些参数都来自配置文件，便于后续调参而不改代码。
        self.embedding_model = retrieval_cfg["embedding_model"]
        self.embedding_dimensions = retrieval_cfg.get("embedding_dimensions", 1024)
        self.top_k = retrieval_cfg["top_k"]
        self.batch_size = retrieval_cfg.get("batch_size", 10)
        self.normalize_embeddings = retrieval_cfg.get("normalize_embeddings", True)

        # chunks 保存原始 chunk，chunk_embeddings 保存每个 chunk 的向量。
        self.chunks: List[DocumentChunk] = []
        self.chunk_embeddings = None

    def _normalize(self, vectors: np.ndarray) -> np.ndarray:
        # 归一化后再做点积，本质上就接近余弦相似度，能让相似度比较更稳定。
        norms = np.linalg.norm(vectors, axis=1, keepdims=True)
        norms[norms == 0] = 1e-12
        return vectors / norms

    def _embed_texts(self, texts: List[str]) -> np.ndarray:
        # 分批请求 embedding，避免一次输入过多文本导致请求过大。
        all_embeddings = []

        for i in range(0, len(texts), self.batch_size):
            batch = texts[i:i + self.batch_size]

            # 调用向量模型，把文本编码成向量。
            resp = self.client.embeddings.create(
                model=self.embedding_model,
                input=batch,
                dimensions=self.embedding_dimensions
            )

            # OpenAI 兼容接口返回的是逐条 embedding，整理成一个列表。
            batch_embeddings = [item.embedding for item in resp.data]
            all_embeddings.extend(batch_embeddings)

        embeddings = np.array(all_embeddings, dtype=np.float32)

        # 如果配置开启，就把 embedding 归一化。
        if self.normalize_embeddings:
            embeddings = self._normalize(embeddings)

        return embeddings

    def build_index(self, chunks: List[DocumentChunk]):
        if not chunks:
            raise ValueError("No chunks provided for dense retriever.")

        # 先保存 chunk，再批量生成所有 chunk 的向量，作为检索索引。
        self.chunks = chunks
        texts = [chunk.text for chunk in chunks]
        self.chunk_embeddings = self._embed_texts(texts)

    def retrieve(self, query: str, top_k: int = None) -> List[RetrievalResult]:
        if self.chunk_embeddings is None or len(self.chunks) == 0:
            raise ValueError("Retriever index is empty. Please call build_index first.")

        # query 也要先转成向量，才能和 chunk 向量比较。
        k = top_k or self.top_k
        query_embedding = self._embed_texts([query])[0]

        # 用点积计算 query 与所有 chunk 的相似度。
        scores = np.dot(self.chunk_embeddings, query_embedding)

        # 分数从高到低排序，取前 k 个。
        top_indices = np.argsort(scores)[::-1][:k]

        results = []
        for idx in top_indices:
            chunk = self.chunks[idx]
            score = float(scores[idx])

            # 把原始 chunk 和相似度分数一起包装成检索结果，方便后续生成和引用。
            results.append(
                RetrievalResult(
                    chunk_id=chunk.chunk_id,
                    text=chunk.text,
                    score=score,
                    source=chunk.source,
                    file_name=chunk.file_name,
                    file_type=chunk.file_type,
                    page=chunk.page,
                    retrieval_type="dense",
                )
            )

        return results


class BM25Retriever:
    def __init__(self):
        # BM25 不需要 embedding 模型，只需要 top_k 之类的检索参数。
        retrieval_cfg = load_yaml(RETRIEVAL_CONFIG_PATH)
        self.top_k = retrieval_cfg.get("top_k", 3)

        # tokenized_corpus 是每个 chunk 的分词结果，bm25 是 BM25Okapi 索引。
        self.chunks: List[DocumentChunk] = []
        self.tokenized_corpus = []
        self.bm25 = None

    def build_index(self, chunks: List[DocumentChunk]):
        if not chunks:
            raise ValueError("No chunks provided for BM25 retriever.")

        # 先把每个 chunk 分词，再交给 BM25Okapi 建索引。
        self.chunks = chunks
        self.tokenized_corpus = [simple_tokenize(chunk.text) for chunk in chunks]
        self.bm25 = BM25Okapi(self.tokenized_corpus)

    def retrieve(self, query: str, top_k: int = None) -> List[RetrievalResult]:
        if self.bm25 is None or len(self.chunks) == 0:
            raise ValueError("BM25 index is empty. Please call build_index first.")

        # 把 query 也做同样的分词，再计算 BM25 得分。
        k = top_k or self.top_k
        query_tokens = simple_tokenize(query)

        scores = self.bm25.get_scores(query_tokens)

        # BM25 的结果同样按分数排序，取前 k 个。
        top_indices = np.argsort(scores)[::-1][:k]

        results = []
        for idx in top_indices:
            chunk = self.chunks[idx]
            score = float(scores[idx])

            # 这里标记 retrieval_type="bm25"，后面做 Hybrid 融合时可以区分来源。
            results.append(
                RetrievalResult(
                    chunk_id=chunk.chunk_id,
                    text=chunk.text,
                    score=score,
                    source=chunk.source,
                    file_name=chunk.file_name,
                    file_type=chunk.file_type,
                    page=chunk.page,
                    retrieval_type="bm25",
                )
            )

        return results


class HybridRetriever:
    def __init__(self):
        # Hybrid 检索把 Dense 和 BM25 组合起来，因此需要同时保存两套 retriever。
        retrieval_cfg = load_yaml(RETRIEVAL_CONFIG_PATH)

        # alpha 越大越偏向 Dense，越小越偏向 BM25。
        self.top_k = retrieval_cfg.get("top_k", 3)
        self.hybrid_alpha = retrieval_cfg.get("hybrid_alpha", 0.6)
        self.bm25_top_k = retrieval_cfg.get("bm25_top_k", 10)
        self.dense_top_k = retrieval_cfg.get("dense_top_k", 10)

        self.dense_retriever = QwenDenseRetriever()
        self.bm25_retriever = BM25Retriever()

        # 由于融合阶段只保留 chunk_id 和最终分数，所以这里保留 chunk_id 到 chunk 的映射。
        self.chunk_map: Dict[str, DocumentChunk] = {}

    def build_index(self, chunks: List[DocumentChunk]):
        if not chunks:
            raise ValueError("No chunks provided for hybrid retriever.")

        # 两种检索器都要各自建索引，Hybrid 才能同时拿到 dense 和 bm25 结果。
        self.chunk_map = {chunk.chunk_id: chunk for chunk in chunks}
        self.dense_retriever.build_index(chunks)
        self.bm25_retriever.build_index(chunks)

    def retrieve(self, query: str, top_k: int = None) -> List[RetrievalResult]:
        # 最终返回多少条由 top_k 控制。
        k = top_k or self.top_k

        # 分别跑 Dense 和 BM25，先拿两套候选结果。
        dense_results = self.dense_retriever.retrieve(query, top_k=self.dense_top_k)
        bm25_results = self.bm25_retriever.retrieve(query, top_k=self.bm25_top_k)

        # 先把结果整理成 chunk_id -> score，便于后面做融合。
        dense_scores = {r.chunk_id: r.score for r in dense_results}
        bm25_scores = {r.chunk_id: r.score for r in bm25_results}

        # 归一化是关键步骤：Dense 和 BM25 原始分数量纲不同，直接加权会失衡。
        dense_scores = minmax_normalize(dense_scores)
        bm25_scores = minmax_normalize(bm25_scores)

        # 候选集合取两边结果的并集，这样不会漏掉只在一种检索器中出现的 chunk。
        candidate_ids = set(dense_scores.keys()) | set(bm25_scores.keys())

        final_scores = {}
        for chunk_id in candidate_ids:
            d_score = dense_scores.get(chunk_id, 0.0)
            b_score = bm25_scores.get(chunk_id, 0.0)

            # 线性融合：alpha 控制 Dense 占比，1-alpha 控制 BM25 占比。
            final_scores[chunk_id] = self.hybrid_alpha * d_score + (1 - self.hybrid_alpha) * b_score

        # 融合后的最终分数再排序，取前 k 个作为最终检索结果。
        ranked_ids = sorted(final_scores, key=final_scores.get, reverse=True)[:k]

        results = []
        for chunk_id in ranked_ids:
            chunk = self.chunk_map[chunk_id]

            # 返回的是融合后的结果，但保留原始 chunk 内容，方便后续生成答案和引用。
            results.append(
                RetrievalResult(
                    chunk_id=chunk.chunk_id,
                    text=chunk.text,
                    score=float(final_scores[chunk_id]),
                    source=chunk.source,
                    file_name=chunk.file_name,
                    file_type=chunk.file_type,
                    page=chunk.page,
                    retrieval_type="hybrid",
                )
            )

        return results


def get_retriever_from_config():
    retrieval_cfg = load_yaml(RETRIEVAL_CONFIG_PATH)
    mode = retrieval_cfg.get("retrieval_mode", "dense")

    if mode == "dense":
        return QwenDenseRetriever()

    if mode == "bm25":
        return BM25Retriever()

    if mode == "hybrid":
        return HybridRetriever()

    raise ValueError(f"Unsupported retrieval_mode: {mode}")