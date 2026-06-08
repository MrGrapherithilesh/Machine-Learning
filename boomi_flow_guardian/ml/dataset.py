from pathlib import Path

import pandas as pd


FEATURE_COLUMNS = [
    "volume_per_day",
    "field_count",
    "required_field_count",
    "connector_complexity",
    "schedule_minutes",
    "retry_count",
    "weak_mapping_count",
    "transformation_count",
]


def load_history(path: Path) -> pd.DataFrame:
    return pd.read_csv(path)


def build_feature_row(settings, source_fields, target_fields, connector, mappings):
    weak_count = sum(1 for item in mappings if item.confidence < 0.55)
    transformation_count = sum(1 for item in mappings if item.transformation != "direct")
    required_count = sum(1 for field in target_fields if field.required)
    return {
        "volume_per_day": settings.volume_per_day,
        "field_count": len(source_fields) + len(target_fields),
        "required_field_count": required_count,
        "connector_complexity": connector.get("complexity", 0.55),
        "schedule_minutes": settings.schedule_minutes,
        "retry_count": settings.retry_count,
        "weak_mapping_count": weak_count,
        "transformation_count": transformation_count,
    }

