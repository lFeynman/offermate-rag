from pydantic import BaseModel, Field
from typing import Any,Dict,Optional

class WorkflowResult(BaseModel):
    route: str
    success: bool = True
    result: Dict[str, Any] = Field(default_factory=dict)
    error: Optional[str] = None