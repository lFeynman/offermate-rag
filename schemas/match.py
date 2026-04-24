from pydantic import BaseModel, Field
from typing import List


class MatchResult(BaseModel):
    matched_skills: List[str] = Field(default_factory=list)
    missing_skills: List[str] = Field(default_factory=list)
    suggestions: List[str] = Field(default_factory=list)
    match_score: float = 0.0