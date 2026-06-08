from config import DEFAULT_CATALOG, DEFAULT_HISTORY, OUTPUT_DIR, SCREENSHOT_DIR
from core.catalog import choose_connector, load_connector_catalog
from core.mapper import suggest_mappings
from core.models import FlowSettings, IntegrationPlan
from core.report_writer import write_report
from core.schema_reader import load_schema
from core.validator import validate_flow
from ml.dataset import build_feature_row, load_history
from ml.risk_model import IntegrationRiskModel, risk_band


def estimate_cost(connector, settings: FlowSettings, mapping_count: int, issue_count: int) -> float:
    base = connector.get("base_cost", 70)
    volume_cost = settings.volume_per_day * 0.0022
    mapping_cost = mapping_count * 1.8
    issue_buffer = issue_count * 9.5
    schedule_factor = max(1, 60 / max(settings.schedule_minutes, 5))
    return round(base + volume_cost + mapping_cost + issue_buffer + schedule_factor * 12, 2)


def build_plan(source_path, target_path, settings: FlowSettings, write_outputs=True):
    source_fields = load_schema(source_path)
    target_fields = load_schema(target_path)
    catalog = load_connector_catalog(DEFAULT_CATALOG)
    connector = choose_connector(catalog, settings.system)
    mappings = suggest_mappings(source_fields, target_fields)
    issues = validate_flow(settings, mappings, target_fields)

    history = load_history(DEFAULT_HISTORY)
    model = IntegrationRiskModel().fit(history)
    feature_row = build_feature_row(settings, source_fields, target_fields, connector, mappings)
    risk_score, runtime_minutes = model.predict(feature_row)
    if any(issue.severity == "high" for issue in issues):
        risk_score = min(0.98, risk_score + 0.12)

    cost = estimate_cost(connector, settings, len(mappings), len(issues))
    summary = {
        "source_fields": len(source_fields),
        "target_fields": len(target_fields),
        "mapping_count": len(mappings),
        "validation_issue_count": len(issues),
        "model_metrics": model.metrics,
        "feature_row": feature_row,
    }
    plan = IntegrationPlan(
        title=f"{settings.system.title()} Customer Sync Plan",
        connector_name=connector["name"],
        flow_settings=settings,
        mappings=mappings,
        validation_issues=issues,
        risk_score=round(risk_score, 3),
        risk_band=risk_band(risk_score),
        runtime_minutes=runtime_minutes,
        estimated_monthly_cost=cost,
        summary=summary,
    )
    artifacts = write_report(plan, OUTPUT_DIR, SCREENSHOT_DIR) if write_outputs else {}
    return plan, artifacts

