from agent.workflow import run_workflow


def test_workflow_skill_matcher():
    jd_text = "岗位要求：熟悉 Python、RAG、FastAPI。"
    resume_text = "技能：Python, RAG。"

    result = run_workflow(
        query="我的简历和岗位匹配吗",
        jd_text=jd_text,
        resume_text=resume_text
    )

    assert result["route"] == "skill_matcher"
    assert "matched_skills" in result["result"]


def test_workflow_jd_parser():
    result = run_workflow(
        query="这个岗位要求哪些技能",
        jd_text="岗位要求：熟悉 Python、RAG。"
    )

    assert result["route"] == "jd_parser"
    assert "required_skills" in result["result"]