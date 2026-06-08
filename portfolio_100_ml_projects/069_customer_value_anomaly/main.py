from pathlib import Path
import sys

PROJECT_ID = 69
PROJECT_TITLE = 'Customer Value Anomaly Detector'
PROJECT_DOMAIN = 'customer value'
PROJECT_KIND = 'anomaly'

COLLECTION_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(COLLECTION_DIR))

from common.project_runner import (  # noqa: E402
    run_anomaly,
    run_classification,
    run_clustering,
    run_forecasting,
    run_nlp,
    run_recommendation,
    run_regression,
)

RUNNERS = {
    'classification': run_classification,
    'regression': run_regression,
    'clustering': run_clustering,
    'forecasting': run_forecasting,
    'nlp': run_nlp,
    'anomaly': run_anomaly,
    'recommendation': run_recommendation,
}


def run_pipeline():
    project_dir = Path(__file__).resolve().parent
    return RUNNERS[PROJECT_KIND](PROJECT_ID, PROJECT_TITLE, PROJECT_DOMAIN, project_dir)


if __name__ == '__main__':
    print(run_pipeline())
