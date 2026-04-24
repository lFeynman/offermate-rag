from pathlib import Path
import yaml


CONFIG_PATH = Path(__file__).resolve().parent.parent / "config" / "workflow.yaml"


def load_route_config():
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def route_query(query: str):
    config = load_route_config()
    routes = config.get("routes", {})
    default_route = config.get("default_route", "rag")

    query_lower = query.lower()
    matched_routes = []

    for route_name, route_info in routes.items():
        keywords = route_info.get("keywords", [])
        priority = route_info.get("priority", 0)

        for kw in keywords:
            if kw.lower() in query_lower:
                matched_routes.append((route_name, priority, kw))
                break

    if not matched_routes:
        return default_route

    matched_routes.sort(key=lambda x: x[1], reverse=True)
    return matched_routes[0][0]