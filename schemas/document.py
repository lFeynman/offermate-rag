from pydantic import BaseModel
from typing import Optional, Dict


class DocumentChunk(BaseModel):
    chunk_id: str
    text: str
    source: str
    file_name: str
    file_type: str
    page: Optional[int] = None
    extra_metadata: Dict = {}