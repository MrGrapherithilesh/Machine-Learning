import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "backend"))

from app.ml.dataset import generate_synthetic_biomarker_dataset


if __name__ == "__main__":
    dataset = generate_synthetic_biomarker_dataset()
    print(f"Generated dataset with {len(dataset)} rows.")
