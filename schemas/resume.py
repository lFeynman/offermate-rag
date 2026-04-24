from pydantic import BaseModel, Field
from typing import List, Optional


class ProjectInfo(BaseModel):
    name: str
    description: Optional[str] = None
    skills: List[str] = Field(default_factory=list)


class ResumeInfo(BaseModel):
    name: Optional[str] = None
    education: List[str] = Field(default_factory=list)
    skills: List[str] = Field(default_factory=list)
    projects: List[ProjectInfo] = Field(default_factory=list)
    awards: List[str] = Field(default_factory=list)