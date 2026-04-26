from tools.jd_parser import parse_jd


def test_parse_jd_extract_skills():
    text = """
    岗位名称：大模型算法实习生
    岗位要求：熟悉 Python、RAG、FastAPI，了解大模型应用。
    学历要求：本科及以上
    实习 6 个月以上
    """

    result = parse_jd(text)

    all_skills = result.required_skills + result.preferred_skills
    assert "Python" in all_skills
    assert "RAG" in all_skills
    assert result.degree_requirement is not None