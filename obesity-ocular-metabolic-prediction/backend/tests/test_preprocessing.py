import pandas as pd

from app.core.config import BASE_FEATURES
from app.ml.dataset import generate_synthetic_biomarker_dataset
from app.ml.preprocessing import FeatureEngineer, build_preprocessor


def test_feature_engineering_adds_clinical_ratios(tmp_path):
    df = generate_synthetic_biomarker_dataset(path=tmp_path / "dataset.csv", n_samples=80)
    engineered = FeatureEngineer().transform(df[BASE_FEATURES])

    assert "pulse_pressure" in engineered.columns
    assert "cholesterol_ratio" in engineered.columns
    assert "ocular_vascular_index" in engineered.columns


def test_preprocessor_handles_missing_values(tmp_path):
    df = generate_synthetic_biomarker_dataset(path=tmp_path / "dataset.csv", n_samples=80)
    X = df[BASE_FEATURES].copy()
    X.loc[X.index[:3], "bmi"] = pd.NA

    preprocessor = build_preprocessor()
    transformed = preprocessor.fit_transform(X)

    assert transformed.shape[0] == len(X)
    assert transformed.shape[1] > len(BASE_FEATURES)
