from pydantic import BaseModel, Field
from typing import List, Optional


class JDInfo(BaseModel):
    job_title: Optional[str] = None
    company: Optional[str] = None
    responsibilities: List[str] = Field(default_factory=list)
    required_skills: List[str] = Field(default_factory=list)
    preferred_skills: List[str] = Field(default_factory=list)
    degree_requirement: Optional[str] = None
    internship_duration: Optional[str] = None