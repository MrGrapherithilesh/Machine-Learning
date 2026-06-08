# Boomi Flow Guardian

Boomi Flow Guardian is a Python ML project by Mithilesh for planning integration flows before building them in Boomi. The idea is simple: give the tool a source schema, a target schema, and basic flow settings, then it suggests field mappings, estimates risk, validates common integration mistakes, and prepares a clean report.

I made this project because integration work usually has many small mistakes like missing required fields, wrong transformations, weak retry rules, or unclear connector choices. This project tries to catch those issues early using Python, rules, and machine learning.

## Features

- Source to target field mapping suggestions
- Connector catalog for common business systems
- ML-based integration risk scoring
- Runtime and cost estimation
- Flow validation with severity levels
- Flask dashboard for reviewing a flow
- Command-line report generation
- Sample schemas and historical run data
- Tests for planner, mapper, validation, and ML pipeline
- Screenshot-friendly dashboard output

## Tech Stack

- Python
- Flask
- Pandas
- NumPy
- Scikit-learn
- Matplotlib
- Pytest

## Project Structure

```text
boomi_flow_guardian/
├── app/
├── core/
├── ml/
├── data/
├── templates/
├── static/
├── outputs/
├── screenshots/
├── tests/
├── main.py
├── cli.py
└── requirements.txt
```

## Run Locally

```bash
cd boomi_flow_guardian
pip install -r requirements.txt
python main.py
```

Open:

```text
http://127.0.0.1:5008
```

## CLI Report

```bash
python cli.py --source data/source_customer_schema.json --target data/target_crm_schema.json --system salesforce --volume 18000
```

The report is saved inside `outputs/`.

## Tests

```bash
pytest tests
```

## Outputs

- `outputs/integration_report.json`
- `outputs/mapping_suggestions.csv`
- `outputs/boomi_process_blueprint.json`
- `outputs/risk_chart.png`
- `screenshots/dashboard_preview.html`

## What I Learned

- How schema matching can be improved with text similarity
- How ML can score operational risk from historical run data
- How integration projects can be validated before implementation
- How to combine Flask, Scikit-learn, and clean Python modules in one practical tool

## Author

Mithilesh
