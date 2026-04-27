from agent.workflow import run_workflow


def run_workflow_check():
    jd_text = """
    岗位名称：大模型算法实习生
    岗位要求：熟悉 Python、RAG、FastAPI，了解大模型应用。
    加分项：Docker、Linux。
    """

    resume_text = """
    张三
    教育背景：合肥工业大学 信息安全 本科
    技能：Python, RAG, FastAPI
    项目：OfferMate-RAG 智能求职助手
    """

    cases = [
        "这个岗位要求哪些技能",
        "帮我解析这份简历",
        "我的简历和这个岗位匹配吗",
        "根据我的简历和岗位 JD 生成面试题",
        "这篇技术文档讲了什么"
    ]

    for query in cases:
        result = run_workflow(
            query=query,
            jd_text=jd_text,
            resume_text=resume_text
        )

        print("=" * 60)
        print("Query:", query)
        print("Route:", result.route)
        print("Success:", result.success)
        print("Error:", result.error)
        print("Result:", result.result)