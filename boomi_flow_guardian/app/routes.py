from flask import Blueprint, render_template, request

from config import DEFAULT_SOURCE_SCHEMA, DEFAULT_TARGET_SCHEMA
from core.models import FlowSettings
from core.planner import build_plan

bp = Blueprint("main", __name__)


@bp.route("/", methods=["GET", "POST"])
def dashboard():
    settings = FlowSettings(system="salesforce", volume_per_day=18000, schedule_minutes=15, retry_count=3)
    if request.method == "POST":
        settings = FlowSettings(
            system=request.form.get("system", "salesforce"),
            volume_per_day=int(request.form.get("volume_per_day", "18000")),
            schedule_minutes=int(request.form.get("schedule_minutes", "15")),
            retry_count=int(request.form.get("retry_count", "3")),
            has_dead_letter=request.form.get("has_dead_letter") == "on",
            encryption_enabled=request.form.get("encryption_enabled") == "on",
        )
    plan, artifacts = build_plan(DEFAULT_SOURCE_SCHEMA, DEFAULT_TARGET_SCHEMA, settings, write_outputs=True)
    return render_template("dashboard.html", plan=plan, artifacts=artifacts)

