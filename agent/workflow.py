from agent.router import route_query
from agent.registry import get_tool
from schemas.agent import WorkflowResult


from agent.router import route_query
from agent.registry import get_tool, get_tool_spec
from schemas.agent import WorkflowResult


def _model_to_dict(obj):
    if hasattr(obj, "model_dump"):
        return obj.model_dump()
    if isinstance(obj, dict):
        return obj
    return {"value": obj}


def _validate_required_inputs(route: str, jd_text: str, resume_text: str, doc_text: str):
    spec = get_tool_spec(route)

    if not spec:
        return True, None

    required_inputs = spec.get("required_inputs", [])

    input_map = {
        "jd_text": jd_text,
        "resume_text": resume_text,
        "doc_text": doc_text,
    }

    missing = []
    for item in required_inputs:
        if not input_map.get(item, "").strip():
            missing.append(item)

    if missing:
        return False, f"Missing required inputs for {route}: {missing}"

    return True, None


def run_workflow(
    query: str,
    jd_text: str = "",
    resume_text: str = "",
    doc_text: str = ""
) -> WorkflowResult:
    route = route_query(query)

    if route == "rag":
        return WorkflowResult(
            route="rag",
            success=True,
            result={
                "message": "该请求应进入 RAG 问答流程。"
            }
        )

    tool = get_tool(route)

    if tool is None:
        return WorkflowResult(
            route=route,
            success=False,
            result={},
            error=f"Tool not found: {route}"
        )

    valid, error = _validate_required_inputs(route, jd_text, resume_text, doc_text)
    if not valid:
        return WorkflowResult(
            route=route,
            success=False,
            result={},
            error=error
        )

    try:
        if route == "jd_parser":
            result = tool(jd_text)

        elif route == "resume_parser":
            result = tool(resume_text)

        elif route == "skill_matcher":
            result = tool(jd_text, resume_text)

        elif route == "interview_generator":
            result = tool(jd_text, resume_text)

        else:
            return WorkflowResult(
                route=route,
                success=False,
                result={},
                error=f"Unsupported route: {route}"
            )

        return WorkflowResult(
            route=route,
            success=True,
            result=_model_to_dict(result),
            error=None
        )

    except Exception as e:
        return WorkflowResult(
            route=route,
            success=False,
            result={},
            error=str(e)
        )