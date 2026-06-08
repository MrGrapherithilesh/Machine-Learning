# Customer Segmentation Lab

Groups customers using spending, visit, income, and loyalty signals.

This project is part of Mithilesh's machine learning portfolio. I kept it small enough to run quickly, but complete enough to show the full flow from data preparation to model output and visual reporting.

## What It Does

- Builds or loads a compact sample dataset
- Trains a machine learning pipeline
- Saves model output and metrics
- Creates a chart for quick review
- Includes a screenshot-friendly HTML preview
- Includes a basic pytest check

## Tech Stack

- Python
- NumPy
- Pandas
- Scikit-learn
- Matplotlib
- Joblib
- Pytest

## Folder Structure

```text
customer_segmentation_lab/
├── main.py
├── requirements.txt
├── outputs/
├── screenshots/
├── models/
└── tests/
```

## How To Run

```bash
cd customer_segmentation_lab
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py
```

## Run Tests

```bash
pytest tests
```

## Outputs

- `outputs/metrics.json`
- `outputs/run_log.txt`
- Prediction or report CSV inside `outputs/`
- `screenshots/dashboard.png`
- `screenshots/ui_preview.html`

## Notes

I designed this project for quick interview demos. The dataset is intentionally lightweight so the complete run finishes fast on a normal laptop.

## Author

Mithilesh
