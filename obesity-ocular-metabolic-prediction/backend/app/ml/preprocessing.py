from __future__ import annotations

from typing import Self

import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from app.core.config import CATEGORICAL_FEATURES, NUMERIC_FEATURES


class FeatureEngineer(BaseEstimator, TransformerMixin):
    """Create compact clinical features from raw biomarkers."""

    def fit(self, X: pd.DataFrame, y: pd.Series | None = None) -> Self:
        return self

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        frame = X.copy()
        frame["pulse_pressure"] = frame["systolic_bp"] - frame["diastolic_bp"]
        frame["cholesterol_ratio"] = frame["total_cholesterol_mg_dl"] / frame["hdl_mg_dl"].replace(0, np.nan)
        frame["waist_height_ratio"] = frame["waist_circumference_cm"] / frame["height_cm"].replace(0, np.nan)
        frame["metabolic_load_score"] = (
            frame["bmi"] * 0.25
            + frame["fasting_glucose_mg_dl"] * 0.02
            + frame["triglycerides_mg_dl"] * 0.01
            + frame["insulin_resistance_index"] * 0.6
        )
        frame["ocular_vascular_index"] = (
            (1 - frame["arteriole_venule_ratio"]) * 10
            + frame["ocular_risk_score"] * 0.08
            + frame["intraocular_pressure_mmhg"] * 0.05
        )
        return frame


class IQRClipper(BaseEstimator, TransformerMixin):
    """Clip numeric outliers using fitted interquartile ranges."""

    def __init__(self, multiplier: float = 1.5) -> None:
        self.multiplier = multiplier
        self.lower_bounds_: np.ndarray | None = None
        self.upper_bounds_: np.ndarray | None = None

    def fit(self, X: np.ndarray, y: pd.Series | None = None) -> Self:
        q1 = np.nanpercentile(X, 25, axis=0)
        q3 = np.nanpercentile(X, 75, axis=0)
        iqr = q3 - q1
        self.lower_bounds_ = q1 - self.multiplier * iqr
        self.upper_bounds_ = q3 + self.multiplier * iqr
        return self

    def transform(self, X: np.ndarray) -> np.ndarray:
        if self.lower_bounds_ is None or self.upper_bounds_ is None:
            raise RuntimeError("IQRClipper must be fitted before transform.")
        return np.clip(X, self.lower_bounds_, self.upper_bounds_)

    def get_feature_names_out(self, input_features: np.ndarray | list[str] | None = None) -> np.ndarray:
        if input_features is None:
            return np.array([], dtype=object)
        return np.asarray(input_features, dtype=object)


def build_preprocessor() -> Pipeline:
    """Build the preprocessing pipeline used by all classifiers."""

    numeric_pipeline = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("outlier_clipper", IQRClipper(multiplier=1.5)),
            ("scaler", StandardScaler()),
        ]
    )

    categorical_pipeline = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("encoder", OneHotEncoder(handle_unknown="ignore")),
        ]
    )

    column_transformer = ColumnTransformer(
        transformers=[
            ("num", numeric_pipeline, NUMERIC_FEATURES),
            ("cat", categorical_pipeline, CATEGORICAL_FEATURES),
        ]
    )

    return Pipeline(
        steps=[
            ("feature_engineering", FeatureEngineer()),
            ("preprocessor", column_transformer),
        ]
    )


def get_transformed_feature_names(preprocessor: Pipeline) -> list[str]:
    """Return feature names after engineering and one-hot encoding."""

    column_transformer = preprocessor.named_steps["preprocessor"]
    names = column_transformer.get_feature_names_out()
    return [name.replace("num__", "").replace("cat__", "") for name in names]
