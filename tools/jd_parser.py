import re
from schemas.jd import JDInfo


SKILL_LEXICON = [
    "Python", "Java", "C++", "PyTorch", "TensorFlow", "Transformers",
    "RAG", "Agent", "LangChain", "LlamaIndex", "FastAPI", "Streamlit",
    "Flask", "Linux", "Git", "Docker", "Kubernetes", "SQL",
    "BM25", "Reranker", "Embedding", "向量检索", "混合检索",
    "大模型", "多模态", "Qwen", "LLaVA", "LoRA", "微调",
    "Prompt", "Prompt Engineering", "机器学习", "深度学习",
    "数据结构", "算法", "CUDA", "Pandas", "NumPy"
]


def extract_skills(text: str) -> list[str]:
    found = []
    lower_text = text.lower()

    for skill in SKILL_LEXICON:
        if skill.lower() in lower_text:
            found.append(skill)

    return sorted(set(found))


def extract_degree_requirement(text: str) -> str | None:
    degree_patterns = [
        "本科及以上", "硕士及以上", "博士", "本科", "硕士", "211", "985"
    ]

    for pattern in degree_patterns:
        if pattern in text:
            return pattern

    return None


def extract_internship_duration(text: str) -> str | None:
    patterns = [
        r"实习\s*\d+\s*个月",
        r"\d+\s*个月以上",
        r"每周\s*\d+\s*天",
        r"一周\s*\d+\s*天",
        r"长期实习",
        r"可长期实习"
    ]

    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            return match.group(0)

    return None


def extract_job_title(text: str) -> str | None:
    lines = [line.strip() for line in text.splitlines() if line.strip()]

    for line in lines[:8]:
        if "岗位" in line or "实习生" in line or "工程师" in line:
            return line[:60]

    return None

def extract_responsibilities(text: str) -> list[str]:
    responsibilities = []
    for line in text.splitlines():
        line = line.strip()
        if any(keyword in line for keyword in ["负责", "参与", "完成", "搭建", "设计"]):
            responsibilities.append(line)

    return responsibilities[:6]

def split_required_and_preferred_skills(text: str, skills: list[str]) -> tuple[list[str], list[str]]:
    preferred_keywords = ["优先", "加分", "了解", "熟悉者优先", "有经验优先"]
    preferred_skills = []
    required_skills = []

    lower_text = text.lower()

    for skill in skills:
        pos = lower_text.find(skill.lower())
        window = text[max(0, pos - 30): pos + 80] if pos != -1 else ""

        if any(keyword in window for keyword in preferred_keywords):
            preferred_skills.append(skill)
        else:
            required_skills.append(skill)

    return sorted(set(required_skills)), sorted(set(preferred_skills))


def parse_jd(text: str) -> JDInfo:
    skills = extract_skills(text)
    required_skills, preferred_skills = split_required_and_preferred_skills(text, skills)

    return JDInfo(
        job_title=extract_job_title(text),
        company=None,
        responsibilities=extract_responsibilities(text),
        required_skills=required_skills,
        preferred_skills=preferred_skills,
        degree_requirement=extract_degree_requirement(text),
        internship_duration=extract_internship_duration(text)
    )