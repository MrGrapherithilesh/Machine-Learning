import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "backend"))

from app.ml.training import train_all_models


if __name__ == "__main__":
    artifact = train_all_models()
    print(f"Best model: {artifact['best_model_name']}")
