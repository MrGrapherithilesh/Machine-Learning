from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd
from sklearn.pipeline import Pipeline

from app.ml.preprocessing import get_transformed_feature_names


@dataclass
class FeatureImportance:
    feature: str
    importance: float
    method: str


def _model_importance(model: object) -> np.ndarray | None:
    if hasattr(model, "feature_importances_"):
        return np.asarray(model.feature_importances_, dtype=float)
    if hasattr(model, "coef_"):
        coefficients = np.asarray(model.coef_, dtype=float)
        return np.mean(np.abs(coefficients), axis=0)
    return None


def compute_feature_importance(pipeline: Pipeline, X_sample: pd.DataFrame) -> list[FeatureImportance]:
    """Compute SHAP ranking when available, with a model-importance fallback."""

    preprocessor = pipeline.named_steps["preprocessor"]
    model = pipeline.named_steps["classifier"]
    feature_names = get_transformed_feature_names(preprocessor)
    transformed = preprocessor.transform(X_sample)

    try:
        import shap

        explainer = shap.Explainer(model, transformed)
        shap_values = explainer(transformed)
        values = np.asarray(shap_values.values)
        if values.ndim == 3:
            importance = np.mean(np.abs(values), axis=(0, 2))
        else:
            importance = np.mean(np.abs(values), axis=0)
        method = "SHAP mean absolute value"
    except Exception:
        importance = _model_importance(model)
        method = "model feature importance fallback"

    if importance is None:
        importance = np.zeros(len(feature_names), dtype=float)
        method = "unavailable"

    total = float(np.sum(np.abs(importance))) or 1.0
    normalized = np.abs(importance) / total
    rows = [
        FeatureImportance(feature=feature, importance=float(score), method=method)
        for feature, score in zip(feature_names, normalized, strict=False)
    ]
    rows.sort(key=lambda item: item.importance, reverse=True)
    return rows
