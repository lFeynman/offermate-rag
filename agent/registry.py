from tools.jd_parser import parse_jd
from tools.resume_parser import parse_resume
from tools.skill_matcher import match_skills
from tools.interview_generator import generate_interview_questions


TOOL_REGISTRY = {
    "jd_parser": parse_jd,
    "resume_parser": parse_resume,
    "skill_matcher": match_skills,
    "interview_generator": generate_interview_questions,
}


def get_tool(tool_name: str):
    return TOOL_REGISTRY.get(tool_name)