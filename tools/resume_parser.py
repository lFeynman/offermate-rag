from schemas.resume import ResumeInfo, ProjectInfo
from tools.jd_parser import extract_skills


def extract_name(text: str) -> str | None:
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    if not lines:
        return None

    first_line = lines[0]
    if len(first_line) <= 10 and not any(ch.isdigit() for ch in first_line):
        return first_line

    return None


def extract_education(text: str) -> list[str]:
    education = []

    for line in text.splitlines():
        line = line.strip()
        if any(keyword in line for keyword in ["大学", "学院", "本科", "硕士", "博士", "信息安全", "计算机", "软件工程"]):
            education.append(line)

    return education[:6]


def extract_awards(text: str) -> list[str]:
    awards = []

    for line in text.splitlines():
        line = line.strip()
        if any(keyword in line for keyword in ["奖", "竞赛", "获奖", "银奖", "三等奖", "二等奖", "一等奖", "软著"]):
            awards.append(line)

    return awards[:6]


def extract_projects(text: str) -> list[ProjectInfo]:
    projects = []

    for line in text.splitlines():
        line = line.strip()

        if any(keyword in line for keyword in ["项目", "系统", "平台", "RAG", "幻觉抑制", "助手", "OfferMate", "HSV"]):
            skills = extract_skills(line)
            projects.append(
                ProjectInfo(
                    name=line[:50],
                    description=line,
                    skills=skills
                )
            )

    return projects[:6]


def parse_resume(text: str) -> ResumeInfo:
    skills = extract_skills(text)

    return ResumeInfo(
        name=extract_name(text),
        education=extract_education(text),
        skills=skills,
        projects=extract_projects(text),
        awards=extract_awards(text)
    )