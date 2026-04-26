from tools.interview_generator import generate_interview_questions


def test_generate_interview_questions():
    jd_text = """
    岗位要求：熟悉 Python、RAG、FastAPI。
    """

    resume_text = """
    技能：Python, RAG
    项目：OfferMate-RAG 智能求职助手
    """

    result = generate_interview_questions(jd_text, resume_text)

    assert "basic_questions" in result
    assert "skill_questions" in result
    assert "gap_questions" in result
    assert "project_questions" in result
    assert len(result["basic_questions"]) > 0