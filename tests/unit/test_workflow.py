from agent.workflow import run_workflow
from schemas.agent import WorkflowResult


def test_workflow_skill_matcher():
    jd_text = "岗位要求：熟悉 Python、RAG、FastAPI。"
    resume_text = "技能：Python, RAG。"

    result = run_workflow(
        query="我的简历和岗位匹配吗",
        jd_text=jd_text,
        resume_text=resume_text
    )

    assert isinstance(result, WorkflowResult)
    assert result.route == "skill_matcher"
    assert result.success is True
    assert "matched_skills" in result.result


def test_workflow_jd_parser():
    result = run_workflow(
        query="这个岗位要求哪些技能",
        jd_text="岗位要求：熟悉 Python、RAG。"
    )

    assert isinstance(result, WorkflowResult)
    assert result.route == "jd_parser"
    assert result.success is True
    assert "required_skills" in result.result