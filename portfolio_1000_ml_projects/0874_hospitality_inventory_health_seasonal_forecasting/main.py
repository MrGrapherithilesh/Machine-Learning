from pathlib import Path
import sys

PROJECT_ID = 874
PROJECT_TITLE = 'Hospitality Inventory Health Seasonal Forecaster'
PROJECT_INDUSTRY = 'hospitality'
PROJECT_SUBJECT = 'inventory health'
PROJECT_KIND = 'seasonal_forecasting'

COLLECTION_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(COLLECTION_DIR))

from common.project_runner import run_project  # noqa: E402


def run_pipeline():
    project_dir = Path(__file__).resolve().parent
    return run_project(PROJECT_ID, PROJECT_TITLE, PROJECT_INDUSTRY, PROJECT_SUBJECT, PROJECT_KIND, project_dir)


if __name__ == '__main__':
    print(run_pipeline())
