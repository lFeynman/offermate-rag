from pydantic import BaseModel
from typing import Optional


class RetrievalResult(BaseModel):
    chunk_id: str
    text: str
    score: float
    source: str
    file_name: str
    file_type: str
    page: Optional[int] = None