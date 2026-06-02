from app.ml.dataset import generate_synthetic_biomarker_dataset
from app.ml.training import train_all_models


def test_training_creates_metrics_and_best_model(tmp_path):
    dataset_path = tmp_path / "biomarkers.csv"
    generate_synthetic_biomarker_dataset(path=dataset_path, n_samples=180)

    artifact = train_all_models(data_path=dataset_path, persist=False)

    assert artifact["best_model_name"] in artifact["metrics"]
    assert "Random Forest" in artifact["metrics"]
    assert "XGBoost" in artifact["metrics"]
    assert artifact["feature_importance"]
