from tools.skill_matcher import match_skills


def test_match_skills_basic():
    jd_text = """
    岗位要求：熟悉 Python、RAG、FastAPI、Docker。
    """

    resume_text = """
    技能：Python, RAG, FastAPI
    项目：做过 RAG 智能问答项目。
    """

    result = match_skills(jd_text, resume_text)

    assert "Python" in result.matched_skills
    assert "RAG" in result.matched_skills
    assert "Docker" in result.missing_skills
    assert result.match_score > 0