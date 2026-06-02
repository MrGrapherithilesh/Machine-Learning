from app.core.config import TARGET_COLUMN
from app.ml.dataset import generate_synthetic_biomarker_dataset


def test_dataset_generation_has_expected_columns(tmp_path):
    dataset_path = tmp_path / "biomarkers.csv"
    df = generate_synthetic_biomarker_dataset(path=dataset_path, n_samples=140)

    assert dataset_path.exists()
    assert TARGET_COLUMN in df.columns
    assert {"Low", "Moderate", "High"}.issubset(set(df[TARGET_COLUMN]))
    assert "ocular_risk_score" in df.columns
    assert "insulin_resistance_index" in df.columns
