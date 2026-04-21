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

    for route_name, route_info in routes.items():
        keywords = route_info.get("keywords", [])
        for kw in keywords:
            if kw.lower() in query.lower():
                return route_name

    return default_route