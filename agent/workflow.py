from agent.router import route_query
from agent.registry import get_tool


def run_workflow(
    query: str,
    jd_text: str = "",
    resume_text: str = "",
    doc_text: str = ""
):
    route = route_query(query)
    tool = get_tool(route)

    if route == "jd_parser":
        if not jd_text:
            jd_text = doc_text or query
        result = tool(jd_text)
        return {
            "route": route,
            "result": result.model_dump()
        }

    if route == "resume_parser":
        if not resume_text:
            resume_text = doc_text or query
        result = tool(resume_text)
        return {
            "route": route,
            "result": result.model_dump()
        }

    if route == "skill_matcher":
        result = tool(jd_text, resume_text)
        return {
            "route": route,
            "result": result.model_dump()
        }

    if route == "interview_generator":
        result = tool(jd_text, resume_text)
        return {
            "route": route,
            "result": result
        }

    return {
        "route": "rag",
        "result": {
            "message": "该请求应进入 RAG 问答流程。"
        }
    }