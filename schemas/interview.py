from pydantic import BaseModel, Field
from typing import List


class InterviewQuestionSet(BaseModel):
    basic_questions: List[str] = Field(default_factory=list)
    skill_questions: List[str] = Field(default_factory=list)
    gap_questions: List[str] = Field(default_factory=list)
    project_questions: List[str] = Field(default_factory=list)