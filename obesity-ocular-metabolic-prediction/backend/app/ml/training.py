from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path
from typing import Any

import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import LabelEncoder

from app.core.config import (
    ARTIFACT_DIR,
    BASE_FEATURES,
    FEATURE_IMPORTANCE_PATH,
    METRICS_PATH,
    MODEL_ARTIFACT_PATH,
    TARGET_COLUMN,
)
from app.ml.dataset import load_dataset
from app.ml.explainability import compute_feature_importance
from app.ml.preprocessing import build_preprocessor


def _build_xgboost_model(random_state: int) -> Any:
    try:
        from xgboost import XGBClassifier

        return XGBClassifier(
            objective="multi:softprob",
            eval_metric="mlogloss",
            n_estimators=170,
            max_depth=4,
            learning_rate=0.06,
            subsample=0.9,
            colsample_bytree=0.9,
            random_state=random_state,
        )
    except Exception:
        # TODO: Remove this fallback once XGBoost is installed on every demo machine.
        return GradientBoostingClassifier(random_state=random_state)


def build_model_registry(random_state: int = 42) -> dict[str, Any]:
    """Return candidate classifiers used in the project."""

    return {
        "Logistic Regression": LogisticRegression(max_iter=1500, class_weight="balanced"),
        "Random Forest": RandomForestClassifier(
            n_estimators=220,
            max_depth=11,
            min_samples_leaf=3,
            class_weight="balanced",
            random_state=random_state,
        ),
        "XGBoost": _build_xgboost_model(random_state=random_state),
        "Gradient Boosting": GradientBoostingClassifier(random_state=random_state),
    }


def _evaluate_model(y_true: np.ndarray, probabilities: np.ndarray, predictions: np.ndarray) -> dict[str, float]:
    return {
        "accuracy": round(float(accuracy_score(y_true, predictions)), 4),
        "precision": round(float(precision_score(y_true, predictions, average="weighted", zero_division=0)), 4),
        "recall": round(float(recall_score(y_true, predictions, average="weighted", zero_division=0)), 4),
        "f1": round(float(f1_score(y_true, predictions, average="weighted", zero_division=0)), 4),
        "roc_auc": round(float(roc_auc_score(y_true, probabilities, multi_class="ovr", average="weighted")), 4),
    }


def train_all_models(data_path: Path | None = None, persist: bool = True) -> dict[str, Any]:
    """Train all configured models and persist the best model artifact."""

    ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)
    df = load_dataset(path=data_path) if data_path else load_dataset()
    clean_df = df.dropna(subset=[TARGET_COLUMN]).copy()
    X = clean_df[BASE_FEATURES]
    y = clean_df[TARGET_COLUMN]

    label_encoder = LabelEncoder()
    y_encoded = label_encoder.fit_transform(y)

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y_encoded,
        test_size=0.22,
        random_state=42,
        stratify=y_encoded,
    )

    metrics: dict[str, dict[str, float]] = {}
    fitted_models: dict[str, Pipeline] = {}

    for model_name, classifier in build_model_registry().items():
        pipeline = Pipeline(
            steps=[
                ("preprocessor", build_preprocessor()),
                ("classifier", classifier),
            ]
        )
        try:
            pipeline.fit(X_train, y_train)
        except Exception:
            if model_name != "XGBoost":
                raise
            pipeline = Pipeline(
                steps=[
                    ("preprocessor", build_preprocessor()),
                    ("classifier", GradientBoostingClassifier(random_state=42)),
                ]
            )
            pipeline.fit(X_train, y_train)
        probabilities = pipeline.predict_proba(X_test)
        predictions = pipeline.predict(X_test)
        metrics[model_name] = _evaluate_model(y_test, probabilities, predictions)
        fitted_models[model_name] = pipeline

    best_model_name = max(metrics, key=lambda name: (metrics[name]["f1"], metrics[name]["roc_auc"]))
    best_pipeline = fitted_models[best_model_name]
    feature_importance = compute_feature_importance(best_pipeline, X_train.sample(min(120, len(X_train)), random_state=42))

    artifact = {
        "best_model_name": best_model_name,
        "model": best_pipeline,
        "models": fitted_models,
        "metrics": metrics,
        "classes": label_encoder.classes_.tolist(),
        "feature_importance": [asdict(item) for item in feature_importance],
        "training_records": int(len(clean_df)),
    }

    if persist:
        joblib.dump(artifact, MODEL_ARTIFACT_PATH)
        METRICS_PATH.write_text(json.dumps(metrics, indent=2), encoding="utf-8")
        FEATURE_IMPORTANCE_PATH.write_text(json.dumps(artifact["feature_importance"], indent=2), encoding="utf-8")
    return artifact


if __name__ == "__main__":
    trained = train_all_models()
    print(f"Best model: {trained['best_model_name']}")
    for name, values in trained["metrics"].items():
        print(f"{name}: {values}")
