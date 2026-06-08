from pathlib import Path

from config import DEFAULT_SOURCE_SCHEMA, DEFAULT_TARGET_SCHEMA
from core.models import FlowSettings
from core.planner import build_plan
from core.schema_reader import load_schema


def test_schema_reader_loads_fields():
    fields = load_schema(DEFAULT_SOURCE_SCHEMA)
    assert len(fields) == 10
    assert fields[0].name == "cust_id"


def test_plan_builds_artifacts():
    settings = FlowSettings(system="salesforce", volume_per_day=18000, schedule_minutes=15, retry_count=3)
    plan, artifacts = build_plan(DEFAULT_SOURCE_SCHEMA, DEFAULT_TARGET_SCHEMA, settings, write_outputs=True)
    assert plan.connector_name == "Salesforce"
    assert len(plan.mappings) == 10
    assert 0 <= plan.risk_score <= 1
    assert plan.risk_band in {"Low", "Medium", "High"}
    assert Path(artifacts["report"]).exists()
    assert Path(artifacts["mapping_csv"]).exists()
    assert Path(artifacts["blueprint"]).exists()
    assert Path(artifacts["chart"]).exists()
    assert Path(artifacts["preview"]).exists()


def test_validation_catches_weak_settings():
    settings = FlowSettings(
        system="netsuite",
        volume_per_day=90000,
        schedule_minutes=60,
        retry_count=1,
        has_dead_letter=False,
        encryption_enabled=False,
    )
    plan, _ = build_plan(DEFAULT_SOURCE_SCHEMA, DEFAULT_TARGET_SCHEMA, settings, write_outputs=False)
    codes = {issue.code for issue in plan.validation_issues}
    assert "SCHEDULE_TOO_SLOW" in codes
    assert "NO_DEAD_LETTER" in codes
    assert "ENCRYPTION_DISABLED" in codes
