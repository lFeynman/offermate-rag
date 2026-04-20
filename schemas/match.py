from pydantic import BaseModel
from typing import List


# 岗位和简历的匹配结果
class MatchResult(BaseModel):
    # 简历中已经覆盖到的技能
    matched_skills: List[str] = []
    # JD 提到但简历里没有覆盖到的技能
    missing_skills: List[str] = []
    # 针对缺口给出的改进建议
    suggestions: List[str] = []