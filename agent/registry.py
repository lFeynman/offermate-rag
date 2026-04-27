from pathlib import Path
import yaml

from tools.jd_parser import parse_jd
from tools.resume_parser import parse_resume
from tools.skill_matcher import match_skills
from tools.interview_generator import generate_interview_questions


TOOL_CONFIG_PATH = Path(__file__).resolve().parent.parent / "config" / "tool.yaml"


TOOL_REGISTRY = {
    "jd_parser": parse_jd,
    "resume_parser": parse_resume,
    "skill_matcher": match_skills,
    "interview_generator": generate_interview_questions,
}


def load_tool_config():
    with open(TOOL_CONFIG_PATH, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def get_tool(tool_name: str):
    return TOOL_REGISTRY.get(tool_name)


def get_tool_spec(tool_name: str):
    config = load_tool_config()
    return config.get("tools", {}).get(tool_name)


def list_tools():
    return list(TOOL_REGISTRY.keys())