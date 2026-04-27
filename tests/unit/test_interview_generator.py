from tools.interview_generator import generate_interview_questions
from schemas.interview import InterviewQuestionSet


def test_generate_interview_questions():
    jd_text = """
    岗位要求：熟悉 Python、RAG、FastAPI。
    """

    resume_text = """
    技能：Python, RAG
    项目：OfferMate-RAG 智能求职助手
    """

    result = generate_interview_questions(jd_text, resume_text)

    assert isinstance(result, InterviewQuestionSet)
    assert len(result.basic_questions) > 0
    assert len(result.skill_questions) > 0
    assert isinstance(result.gap_questions, list)
    assert isinstance(result.project_questions, list)