from schemas.match import MatchResult
from tools.jd_parser import parse_jd
from tools.resume_parser import parse_resume


def normalize_skill(skill: str) -> str:
    return skill.lower().replace(" ", "").replace("-", "")


def match_skills(jd_text: str, resume_text: str) -> MatchResult:
    jd_info = parse_jd(jd_text)
    resume_info = parse_resume(resume_text)

    jd_skills = set(jd_info.required_skills + jd_info.preferred_skills)
    resume_skills = set(resume_info.skills)

    normalized_resume = {normalize_skill(skill): skill for skill in resume_skills}

    matched = []
    missing = []

    for skill in jd_skills:
        norm = normalize_skill(skill)
        if norm in normalized_resume:
            matched.append(skill)
        else:
            missing.append(skill)

    if len(jd_skills) == 0:
        match_score = 0.0
    else:
        match_score = round(len(matched) / len(jd_skills), 4)

    suggestions = []
    for skill in missing:
        suggestions.append(f"建议在简历中补充与 {skill} 相关的项目经历、技术栈或实践描述。")

    return MatchResult(
        matched_skills=sorted(set(matched)),
        missing_skills=sorted(set(missing)),
        suggestions=suggestions,
        match_score=match_score
    )