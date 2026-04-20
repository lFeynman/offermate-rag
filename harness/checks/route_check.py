from agent.router import route_query


# 手工回归检查：验证典型 query 是否被路由到预期工具。
def run_route_check():
    # key 是用户输入，value 是期望的路由结果。
    cases = {
        "这个岗位要求哪些技能": "jd_parser",
        "帮我分析我的简历": "resume_parser",
        "我的简历和这个岗位匹配吗": "skill_matcher",
        "给我生成一些面试题": "interview_generator",
        "这篇技术文档主要讲什么": "rag",
    }

    # 打印预测值与期望值，便于快速人工比对。
    for query, expected in cases.items():
        pred = route_query(query)
        print(f"query={query} | pred={pred} | expected={expected}")