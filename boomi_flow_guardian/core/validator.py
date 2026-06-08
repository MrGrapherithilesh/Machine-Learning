from typing import List

from core.models import FlowSettings, MappingSuggestion, SchemaField, ValidationIssue


def validate_flow(settings: FlowSettings, mappings: List[MappingSuggestion], target_fields: List[SchemaField]) -> List[ValidationIssue]:
    issues = []
    mapped_targets = {item.target_field for item in mappings if item.confidence >= 0.35}
    required_targets = [field for field in target_fields if field.required]

    for field in required_targets:
        if field.name not in mapped_targets:
            issues.append(
                ValidationIssue(
                    severity="high",
                    code="REQ_FIELD_MISSING",
                    message=f"Required target field '{field.name}' does not have a confident mapping.",
                    recommendation="Add a direct mapping or a default value before deployment.",
                )
            )

    weak = [item for item in mappings if item.confidence < 0.42]
    if weak:
        issues.append(
            ValidationIssue(
                severity="medium",
                code="LOW_MAPPING_CONFIDENCE",
                message=f"{len(weak)} field mappings have low confidence.",
                recommendation="Review low-confidence fields and rename source fields where possible.",
            )
        )

    conversions = [item for item in mappings if item.transformation == "review_required"]
    if conversions:
        issues.append(
            ValidationIssue(
                severity="medium",
                code="TYPE_CONVERSION_REVIEW",
                message=f"{len(conversions)} mappings need manual transformation rules.",
                recommendation="Add map functions for date, number, or string normalization.",
            )
        )

    if settings.volume_per_day > 50000 and settings.schedule_minutes > 30:
        issues.append(
            ValidationIssue(
                severity="high",
                code="SCHEDULE_TOO_SLOW",
                message="High daily volume with a slow schedule may create backlog.",
                recommendation="Run this process every 5 to 15 minutes or use batching.",
            )
        )

    if settings.retry_count < 2:
        issues.append(
            ValidationIssue(
                severity="medium",
                code="RETRY_POLICY_WEAK",
                message="Retry count is low for a business integration.",
                recommendation="Use at least 2 retries with clear error logging.",
            )
        )

    if not settings.has_dead_letter:
        issues.append(
            ValidationIssue(
                severity="high",
                code="NO_DEAD_LETTER",
                message="Failed records do not have a holding area.",
                recommendation="Store failed payloads for replay and support analysis.",
            )
        )

    if not settings.encryption_enabled:
        issues.append(
            ValidationIssue(
                severity="high",
                code="ENCRYPTION_DISABLED",
                message="Sensitive integration data should be encrypted in transit.",
                recommendation="Enable TLS and secure credential storage.",
            )
        )

    if not issues:
        issues.append(
            ValidationIssue(
                severity="info",
                code="FLOW_READY",
                message="No major design issues were detected.",
                recommendation="Run a test batch with sample payloads before release.",
            )
        )
    return issues

