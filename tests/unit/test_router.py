from agent.router import route_query


# 覆盖“岗位匹配”语义，预期路由到 skill_matcher。
def test_route_skill_match():
    assert route_query("我的简历和岗位匹配吗") == "skill_matcher"


# 覆盖通用技术问答语义，未命中特定工具时应走 rag。
def test_route_rag():
    assert route_query("这篇技术文档讲了什么") == "rag"