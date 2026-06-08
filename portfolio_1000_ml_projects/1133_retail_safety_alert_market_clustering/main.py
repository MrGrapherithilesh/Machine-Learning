from pathlib import Path
import sys

PROJECT_ID = 1133
PROJECT_TITLE = 'Retail Safety Alert Segmentation Model'
PROJECT_INDUSTRY = 'retail'
PROJECT_SUBJECT = 'safety alert'
PROJECT_KIND = 'market_clustering'

COLLECTION_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(COLLECTION_DIR))

from common.project_runner import run_project  # noqa: E402


def run_pipeline():
    project_dir = Path(__file__).resolve().parent
    return run_project(PROJECT_ID, PROJECT_TITLE, PROJECT_INDUSTRY, PROJECT_SUBJECT, PROJECT_KIND, project_dir)


if __name__ == '__main__':
    print(run_pipeline())
