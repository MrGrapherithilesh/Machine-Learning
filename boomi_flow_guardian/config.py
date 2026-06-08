from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "outputs"
SCREENSHOT_DIR = BASE_DIR / "screenshots"

DEFAULT_SOURCE_SCHEMA = DATA_DIR / "source_customer_schema.json"
DEFAULT_TARGET_SCHEMA = DATA_DIR / "target_crm_schema.json"
DEFAULT_HISTORY = DATA_DIR / "historical_integration_runs.csv"
DEFAULT_CATALOG = DATA_DIR / "connector_catalog.json"

APP_PORT = 5008

