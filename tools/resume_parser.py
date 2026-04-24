from schemas.resume import ResumeInfo, ProjectInfo
from tools.jd_parser import extract_skills


def parse_resume(text: str) -> ResumeInfo:
    lines = [line.strip() for line in text.splitlines() if line.strip()]

    name = None
    if lines:
        first_line = lines[0]
        if not any(keyword in first_line for keyword in ["技能", "教育", "项目", "经历", "简历"]):
            name = first_line[:50]

    education = []
    projects = []
    current_project_name = None
    current_project_desc = None

    for line in lines:
        if any(keyword in line for keyword in ["本科", "硕士", "博士", "大学", "学院", "专业", "教育背景"]):
            education.append(line)

        if line.startswith("项目") or "项目：" in line:
            if current_project_name:
                projects.append(
                    ProjectInfo(
                        name=current_project_name,
                        description=current_project_desc,
                        skills=[]
                    )
                )
            current_project_name = line.split("：", 1)[-1].strip() or line
            current_project_desc = None
        elif current_project_name and not any(keyword in line for keyword in ["技能", "教育", "工作", "实习"]):
            current_project_desc = line if current_project_desc is None else f"{current_project_desc} {line}"

    if current_project_name:
        projects.append(
            ProjectInfo(
                name=current_project_name,
                description=current_project_desc,
                skills=[]
            )
        )

    return ResumeInfo(
        name=name,
        education=education,
        skills=extract_skills(text),
        projects=projects,
        awards=[]
    )