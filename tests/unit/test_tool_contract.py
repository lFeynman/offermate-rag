from agent.registry import list_tools, get_tool, get_tool_spec


def test_all_registered_tools_have_specs():
    for tool_name in list_tools():
        assert get_tool(tool_name) is not None
        assert get_tool_spec(tool_name) is not None


def test_skill_matcher_required_inputs():
    spec = get_tool_spec("skill_matcher")
    assert "jd_text" in spec["required_inputs"]
    assert "resume_text" in spec["required_inputs"]