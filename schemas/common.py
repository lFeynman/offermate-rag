from pydantic import AliasChoices, BaseModel, Field
from typing import List, Optional


# 单条引用信息：描述答案依据来自哪个来源，以及定位到文档的哪个位置
class Citation(BaseModel):
    # 来源文件名、文档名或 URL
    source: str
    # 可选页码
    page: Optional[int] = None
    # 可选块编号
    chunk_id: Optional[str] = None


# RAG 问答的统一输出结构，包含答案和支撑答案的引用
class RAGResponse(BaseModel):
    # 模型生成的最终回答文本
    answer: str
    # 支撑回答的证据列表
    citations: List[Citation]
    # 是否有足够证据支撑回答，用于判断答案可信度。
    grounded: bool