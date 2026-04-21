from agent.router import route_query


def test_route_skill_match():
    assert route_query("我的简历和岗位匹配吗") == "skill_matcher"


def test_route_rag():
    assert route_query("这篇技术文档讲了什么") == "rag"