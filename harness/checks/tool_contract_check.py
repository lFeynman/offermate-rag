from agent.registry import list_tools, get_tool_spec, get_tool


def run_tool_contract_check():
    tools = list_tools()

    for tool_name in tools:
        tool = get_tool(tool_name)
        spec = get_tool_spec(tool_name)

        print("=" * 60)
        print(f"Tool: {tool_name}")
        print(f"Callable: {tool is not None}")
        print(f"Spec exists: {spec is not None}")

        if spec:
            print(f"Enabled: {spec.get('enabled')}")
            print(f"Mode: {spec.get('mode')}")
            print(f"Required inputs: {spec.get('required_inputs')}")
            print(f"Output schema: {spec.get('output_schema')}")