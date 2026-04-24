from tools.resume_parser import parse_resume


def test_parse_resume_extract_skills():
    text = """
    张三
    某大学 信息安全 本科
    技能：Python, PyTorch, FastAPI, RAG
    项目：OfferMate-RAG 智能求职助手
    """

    result = parse_resume(text)

    assert "Python" in result.skills
    assert "RAG" in result.skills
    assert len(result.education) > 0