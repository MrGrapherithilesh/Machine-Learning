from __future__ import annotations

from collections import Counter
from statistics import mean

import pandas as pd

from app.core.config import BASE_FEATURES, TARGET_COLUMN
from app.db.database import prediction_distribution, recent_predictions
from app.ml.dataset import load_dataset
from app.services.model_service import model_service


def dashboard_summary() -> dict[str, object]:
    df = load_dataset()
    artifact = model_service.artifact
    best_name = str(artifact["best_model_name"])
    distribution = Counter(df[TARGET_COLUMN])
    stored_distribution = prediction_distribution()

    return {
        "total_records": int(len(df)),
        "average_bmi": round(float(df["bmi"].mean()), 2),
        "dataset_prediction_distribution": dict(distribution),
        "live_prediction_distribution": stored_distribution,
        "model_accuracy": artifact["metrics"][best_name]["accuracy"],
        "best_model": best_name,
        "recent_predictions": recent_predictions(),
    }


def model_metrics() -> list[dict[str, object]]:
    artifact = model_service.artifact
    return [
        {"model_name": model_name, **values}
        for model_name, values in artifact["metrics"].items()
    ]


def analytics_payload() -> dict[str, object]:
    df = load_dataset()
    numeric_df = df[BASE_FEATURES].select_dtypes(include=["number"])
    correlations = numeric_df.corr(numeric_only=True).round(3)
    selected_features = [
        "bmi",
        "waist_circumference_cm",
        "fasting_glucose_mg_dl",
        "triglycerides_mg_dl",
        "insulin_resistance_index",
        "ocular_risk_score",
        "arteriole_venule_ratio",
        "retinal_venule_diameter_um",
    ]
    matrix = [
        {
            "feature": row_feature,
            **{column_feature: float(correlations.loc[row_feature, column_feature]) for column_feature in selected_features},
        }
        for row_feature in selected_features
    ]

    distributions = []
    for column in ["bmi", "fasting_glucose_mg_dl", "ocular_risk_score"]:
        grouped = df.groupby(TARGET_COLUMN)[column].mean(numeric_only=True).round(2)
        distributions.append(
            {
                "feature": column,
                "Low": float(grouped.get("Low", 0)),
                "Moderate": float(grouped.get("Moderate", 0)),
                "High": float(grouped.get("High", 0)),
            }
        )

    return {
        "feature_importance": model_service.artifact.get("feature_importance", [])[:15],
        "correlation_matrix": matrix,
        "distributions": distributions,
    }


def research_insights() -> dict[str, object]:
    df = load_dataset()
    artifact = model_service.artifact
    top_features = artifact.get("feature_importance", [])[:5]
    high_risk = df[df[TARGET_COLUMN] == "High"]

    return {
        "key_findings": [
            "Metabolic load features show the strongest separation between low and high obesity risk groups.",
            "Ocular vascular indicators add useful context beyond BMI by reflecting vessel narrowing and retinal risk.",
            "Tree-based models capture non-linear relationships between glucose, triglycerides, blood pressure, and ocular measurements.",
        ],
        "important_biomarkers": top_features,
        "dataset_statistics": {
            "records": int(len(df)),
            "average_age": round(float(df["age"].mean()), 2),
            "average_bmi": round(float(df["bmi"].mean()), 2),
            "high_risk_average_bmi": round(float(high_risk["bmi"].mean()), 2),
            "risk_categories": dict(Counter(df[TARGET_COLUMN])),
            "missing_values_total": int(df.isna().sum().sum()),
        },
        "student_notes": [
            "TODO: connect the ocular fields to real retinal image extraction in the next version.",
            "The current dataset is synthetic, so the model is a research prototype rather than a clinical tool.",
        ],
        "mean_feature_importance": round(
            mean([float(item["importance"]) for item in top_features]) if top_features else 0,
            4,
        ),
    }
