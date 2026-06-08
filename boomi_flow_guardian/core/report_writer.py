import csv
import json
from dataclasses import asdict
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from core.blueprint import build_process_blueprint


def write_report(plan, output_dir: Path, screenshot_dir: Path):
    output_dir.mkdir(exist_ok=True)
    screenshot_dir.mkdir(exist_ok=True)

    report_path = output_dir / "integration_report.json"
    mapping_path = output_dir / "mapping_suggestions.csv"
    blueprint_path = output_dir / "boomi_process_blueprint.json"
    chart_path = output_dir / "risk_chart.png"
    preview_path = screenshot_dir / "dashboard_preview.html"

    report_path.write_text(json.dumps(asdict(plan), indent=2), encoding="utf-8")
    blueprint_path.write_text(json.dumps(build_process_blueprint(plan), indent=2), encoding="utf-8")
    with mapping_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["source_field", "target_field", "confidence", "transformation", "notes"])
        writer.writeheader()
        for item in plan.mappings:
            writer.writerow(asdict(item))

    make_chart(plan, chart_path)
    make_preview(plan, preview_path)
    return {
        "report": str(report_path),
        "mapping_csv": str(mapping_path),
        "blueprint": str(blueprint_path),
        "chart": str(chart_path),
        "preview": str(preview_path),
    }


def make_chart(plan, chart_path: Path):
    colors = ["#007AFF", "#34C759", "#FF9500"]
    values = [plan.risk_score, min(plan.runtime_minutes / 60, 1), min(plan.estimated_monthly_cost / 500, 1)]
    labels = ["Risk", "Runtime", "Cost"]
    plt.figure(figsize=(8, 4.8))
    plt.bar(labels, values, color=colors)
    plt.ylim(0, 1)
    plt.title(plan.title)
    plt.ylabel("Normalized score")
    plt.grid(axis="y", alpha=0.22)
    plt.tight_layout()
    plt.savefig(chart_path, dpi=140)
    plt.close()


def make_preview(plan, preview_path: Path):
    issue_rows = "".join(
        f"<tr><td>{issue.severity}</td><td>{issue.code}</td><td>{issue.message}</td></tr>" for issue in plan.validation_issues
    )
    mapping_rows = "".join(
        f"<tr><td>{item.source_field}</td><td>{item.target_field}</td><td>{item.confidence:.2f}</td><td>{item.transformation}</td></tr>"
        for item in plan.mappings[:10]
    )
    html = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{plan.title}</title>
  <link rel="stylesheet" href="../static/css/style.css">
</head>
<body>
  <main class="shell">
    <section class="hero">
      <p class="eyebrow">Boomi Flow Guardian</p>
      <h1>{plan.title}</h1>
      <p>Connector: {plan.connector_name}</p>
      <div class="metrics">
        <div><span>{plan.risk_band}</span><small>Risk band</small></div>
        <div><span>{plan.risk_score:.2f}</span><small>Risk score</small></div>
        <div><span>{plan.runtime_minutes:.1f}m</span><small>Runtime</small></div>
        <div><span>${plan.estimated_monthly_cost:.0f}</span><small>Monthly cost</small></div>
      </div>
    </section>
    <section class="grid">
      <article class="panel"><h2>Top Mappings</h2><table>{mapping_rows}</table></article>
      <article class="panel"><h2>Validation</h2><table>{issue_rows}</table></article>
    </section>
  </main>
</body>
</html>"""
    preview_path.write_text(html, encoding="utf-8")
