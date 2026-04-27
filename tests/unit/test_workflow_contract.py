from agent.workflow import run_workflow
from schemas.agent import WorkflowResult


def test_workflow_returns_schema():
    result = run_workflow(
        query="我的简历和岗位匹配吗",
        jd_text="岗位要求：熟悉 Python、RAG、FastAPI。",
        resume_text="技能：Python, RAG。"
    )

    assert isinstance(result, WorkflowResult)
    assert result.route == "skill_matcher"
    assert result.success is True
    assert "matched_skills" in result.result


def test_workflow_missing_required_inputs():
    result = run_workflow(
        query="我的简历和岗位匹配吗",
        jd_text="岗位要求：熟悉 Python、RAG。",
        resume_text=""
    )

    assert result.success is False
    assert result.error is not None