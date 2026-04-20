from pydantic import BaseModel
from typing import List, Optional


# 简历里的单个项目经历，用于和 JD 要求中的技能做细粒度对比
class ProjectInfo(BaseModel):
    # 项目名称
    name: str
    # 项目的简要描述
    description: Optional[str] = None
    # 该项目用到的技能列表
    skills: List[str] = []


# 简历解析结果
class ResumeInfo(BaseModel):
    # 候选人姓名
    name: Optional[str] = None
    # 教育背景列表
    education: List[str] = []
    # 候选人的核心技能集合
    skills: List[str] = []
    # 项目经历，采用结构化对象而不是纯文本
    projects: List[ProjectInfo] = []
    # 奖项或证书信息
    awards: List[str] = []