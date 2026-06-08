from dataclasses import asdict


def build_process_blueprint(plan):
    """Create a practical build blueprint for an integration developer."""
    retry_enabled = plan.flow_settings.retry_count > 0
    steps = [
        {
            "order": 1,
            "shape": "start",
            "name": "Scheduled Start",
            "config": {"schedule_minutes": plan.flow_settings.schedule_minutes},
        },
        {
            "order": 2,
            "shape": "connector",
            "name": f"Read source records for {plan.connector_name}",
            "config": {"batch_size": recommended_batch_size(plan.flow_settings.volume_per_day)},
        },
        {
            "order": 3,
            "shape": "map",
            "name": "Apply suggested field map",
            "config": {"mapping_count": len(plan.mappings), "review_low_confidence": True},
        },
        {
            "order": 4,
            "shape": "decision",
            "name": "Check required fields and business rules",
            "config": {"high_priority_issues": count_issues(plan, "high")},
        },
        {
            "order": 5,
            "shape": "connector",
            "name": f"Upsert into {plan.connector_name}",
            "config": {"retry_enabled": retry_enabled, "retry_count": plan.flow_settings.retry_count},
        },
        {
            "order": 6,
            "shape": "error_route",
            "name": "Route failed records",
            "config": {"dead_letter_enabled": plan.flow_settings.has_dead_letter},
        },
        {
            "order": 7,
            "shape": "notify",
            "name": "Send run summary",
            "config": {"owner": plan.flow_settings.owner, "risk_band": plan.risk_band},
        },
    ]
    return {
        "process_name": plan.title,
        "connector": plan.connector_name,
        "risk_band": plan.risk_band,
        "estimated_runtime_minutes": plan.runtime_minutes,
        "estimated_monthly_cost": plan.estimated_monthly_cost,
        "recommended_steps": steps,
        "mapping_table": [asdict(item) for item in plan.mappings],
        "validation_summary": [asdict(issue) for issue in plan.validation_issues],
    }


def recommended_batch_size(volume_per_day: int) -> int:
    if volume_per_day >= 75000:
        return 1000
    if volume_per_day >= 25000:
        return 500
    return 200


def count_issues(plan, severity: str) -> int:
    return sum(1 for issue in plan.validation_issues if issue.severity == severity)

