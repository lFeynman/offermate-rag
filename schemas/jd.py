from pydantic import BaseModel
from typing import List, Optional


# 岗位 JD 解析结果，把原始文本整理成便于匹配和分析的结构化数据
class JDInfo(BaseModel):
    # 岗位名称
    job_title: Optional[str] = None
    # 公司名称
    company: Optional[str] = None
    # 必须满足的技能要求
    required_skills: List[str] = []
    # 加分项技能
    preferred_skills: List[str] = []
    # 学历要求
    degree_requirement: Optional[str] = None
    # 实习时长要求
    internship_duration: Optional[str] = None