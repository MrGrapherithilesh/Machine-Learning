import json
from pathlib import Path


def load_connector_catalog(path: Path):
    return json.loads(Path(path).read_text(encoding="utf-8"))["connectors"]


def choose_connector(catalog, system_name: str):
    normalized = system_name.strip().lower()
    for connector in catalog:
        aliases = [connector["name"].lower(), *[item.lower() for item in connector.get("aliases", [])]]
        if normalized in aliases:
            return connector
    for connector in catalog:
        if normalized in connector["name"].lower():
            return connector
    return {
        "name": system_name.title(),
        "category": "Custom",
        "auth": "API key",
        "base_cost": 70,
        "complexity": 0.58,
        "notes": "Custom connector profile based on general REST integration assumptions.",
    }

