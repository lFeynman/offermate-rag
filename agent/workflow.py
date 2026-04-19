from agent.router import route_query

def run_workflow(query: str):
    route = route_query(query)
    return f"Current route: {route}"