from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class SchemaField:
    name: str
    data_type: str
    required: bool = False
    description: str = ""
    examples: List[str] = field(default_factory=list)


@dataclass
class FlowSettings:
    system: str
    volume_per_day: int
    schedule_minutes: int = 30
    retry_count: int = 2
    has_dead_letter: bool = True
    encryption_enabled: bool = True
    owner: str = "Mithilesh"


@dataclass
class MappingSuggestion:
    source_field: str
    target_field: str
    confidence: float
    transformation: str
    notes: str


@dataclass
class ValidationIssue:
    severity: str
    code: str
    message: str
    recommendation: str


@dataclass
class IntegrationPlan:
    title: str
    connector_name: str
    flow_settings: FlowSettings
    mappings: List[MappingSuggestion]
    validation_issues: List[ValidationIssue]
    risk_score: float
    risk_band: str
    runtime_minutes: float
    estimated_monthly_cost: float
    summary: Dict[str, object]

