from tools.skill_matcher import match_skills
from tools.jd_parser import parse_jd
from tools.resume_parser import parse_resume


def generate_interview_questions(jd_text: str, resume_text: str) -> dict:
    jd_info = parse_jd(jd_text)
    resume_info = parse_resume(resume_text)
    match_result = match_skills(jd_text, resume_text)

    basic_questions = [
        "请你做一个简短的自我介绍。",
        "请介绍一个你最熟悉的项目，并说明你的具体贡献。",
        "你为什么想投递这个岗位？"
    ]

    skill_questions = []
    for skill in jd_info.required_skills[:5]:
        skill_questions.append(f"你在 {skill} 方面有哪些实践经验？")

    gap_questions = []
    for skill in match_result.missing_skills[:5]:
        gap_questions.append(f"岗位提到了 {skill}，你目前如何理解这个技术？后续准备怎么补足？")

    project_questions = []
    for project in resume_info.projects[:3]:
        project_questions.append(f"请详细介绍项目「{project.name}」的背景、方法和结果。")

    return {
        "basic_questions": basic_questions,
        "skill_questions": skill_questions,
        "gap_questions": gap_questions,
        "project_questions": project_questions
    }