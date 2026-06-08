import json
from pathlib import Path
from typing import List

from core.models import SchemaField


def load_schema(path: Path) -> List[SchemaField]:
    raw = json.loads(Path(path).read_text(encoding="utf-8"))
    fields = []
    for item in raw.get("fields", []):
        fields.append(
            SchemaField(
                name=item["name"],
                data_type=item.get("type", "string"),
                required=bool(item.get("required", False)),
                description=item.get("description", ""),
                examples=item.get("examples", []),
            )
        )
    return fields


def describe_field(field: SchemaField) -> str:
    examples = " ".join(field.examples[:3])
    return f"{field.name} {field.data_type} {field.description} {examples}".strip()

