from tools.skill_matcher import match_skills
from tools.jd_parser import parse_jd
from tools.resume_parser import parse_resume

TECH_QUESTION_BANK = {
    "RAG": [
        "请解释 RAG 的基本流程，以及它相比直接调用大模型的优势。",
        "在 RAG 系统中，chunk size 和 overlap 会如何影响检索效果？",
        "如果检索结果相关性较差，你会从哪些方面排查？"
    ],
    "FastAPI": [
        "你在项目中为什么选择 FastAPI？",
        "FastAPI 后端接口如何与前端或 pipeline 解耦？"
    ],
    "Python": [
        "你在项目中主要用 Python 完成了哪些模块？",
        "如果处理大量文档，Python 代码中需要注意哪些性能问题？"
    ],
    "Embedding": [
        "Embedding 模型在 RAG 中起什么作用？",
        "你如何判断一个 embedding 模型是否适合当前任务？"
    ],
    "BM25": [
        "BM25 和向量检索有什么区别？",
        "为什么很多 RAG 系统会使用混合检索？"
    ],
    "Reranker": [
        "Reranker 在检索链路中解决什么问题？",
        "使用 reranker 会带来哪些额外开销？"
    ],
    "Agent": [
        "你这个项目中的 agent 体现在哪里？",
        "Router 和 Tool Calling 分别解决什么问题？"
    ],
    "Docker": [
        "你是否了解 Docker 在项目部署中的作用？",
        "如果要把这个项目部署成服务，你会如何容器化？"
    ],
    "Qwen": [
        "你为什么选择 Qwen 模型接入该项目？",
        "Qwen Embedding 和 Qwen Generation 在你的项目中分别承担什么角色？"
    ]
}

def generate_skill_questions(skills:list[str]) -> list[str]:
    questions = []
    for skill in skills:
        if skill in TECH_QUESTION_BANK:
            questions.extend(TECH_QUESTION_BANK[skill])
        else:
            questions.append(f"请介绍一下你在 {skill} 方面的经验和理解。")
    return questions

def generate_gap_questions(missing_skills: list[str]) -> list[str]:
    questions = []

    for skill in missing_skills[:5]:
        questions.append(
            f"岗位要求中提到了 {skill}，但你的简历体现较少。如果面试官追问，你会如何解释或补充？"
        )

    return questions

def generate_project_questions(resume_info) -> list[str]:
    questions = []

    for project in resume_info.projects[:3]:
        project_name = project.name

        questions.extend([
            f"请介绍项目「{project_name}」的背景、目标和最终效果。",
            f"你在项目「{project_name}」中主要负责哪些模块？",
            f"项目「{project_name}」中最有技术含量的部分是什么？",
            f"如果让你重新优化项目「{project_name}」，你会优先改进哪里？"
        ])

    return questions

def generate_interview_questions(jd_text: str, resume_text: str) -> dict:
    jd_info = parse_jd(jd_text)
    resume_info = parse_resume(resume_text)
    match_result = match_skills(jd_text, resume_text)

    basic_questions = [
        "请你做一个 1 分钟自我介绍，并突出和岗位最相关的经历。",
        "你为什么想投递这个岗位？",
        "你认为这个岗位最核心的能力要求是什么？",
        "结合你的经历，你认为自己和这个岗位的匹配点在哪里？"
    ]

    skill_questions = generate_skill_questions(
        jd_info.required_skills[:5] + jd_info.preferred_skills[:3]
    )

    gap_questions = generate_gap_questions(match_result.missing_skills)
    project_questions = generate_project_questions(resume_info)
    return {
        "basic_questions": basic_questions,
        "skill_questions": skill_questions,
        "gap_questions": gap_questions,
        "project_questions": project_questions
    }