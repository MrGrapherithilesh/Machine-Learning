import pandas as pd
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.metrics import accuracy_score, mean_absolute_error
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from ml.dataset import FEATURE_COLUMNS


class IntegrationRiskModel:
    def __init__(self):
        self.classifier = Pipeline(
            [
                ("scale", StandardScaler()),
                ("model", RandomForestClassifier(n_estimators=90, random_state=42, max_depth=7)),
            ]
        )
        self.regressor = Pipeline(
            [
                ("scale", StandardScaler()),
                ("model", RandomForestRegressor(n_estimators=100, random_state=42, max_depth=8)),
            ]
        )
        self.metrics = {}

    def fit(self, history):
        x = history[FEATURE_COLUMNS]
        y_risk = history["failed_run"].astype(int)
        y_runtime = history["runtime_minutes"].astype(float)

        x_train, x_test, y_train, y_test = train_test_split(x, y_risk, test_size=0.25, random_state=42, stratify=y_risk)
        self.classifier.fit(x_train, y_train)
        risk_pred = self.classifier.predict(x_test)

        x_train_r, x_test_r, y_train_r, y_test_r = train_test_split(x, y_runtime, test_size=0.25, random_state=42)
        self.regressor.fit(x_train_r, y_train_r)
        runtime_pred = self.regressor.predict(x_test_r)

        self.metrics = {
            "risk_accuracy": round(float(accuracy_score(y_test, risk_pred)), 3),
            "runtime_mae": round(float(mean_absolute_error(y_test_r, runtime_pred)), 2),
            "training_rows": int(len(history)),
        }
        return self

    def predict(self, feature_row):
        row = pd.DataFrame([{col: feature_row[col] for col in FEATURE_COLUMNS}])
        risk_score = float(self.classifier.predict_proba(row)[0][1])
        runtime = float(self.regressor.predict(row)[0])
        return round(risk_score, 3), round(max(runtime, 1.0), 2)


def risk_band(score: float) -> str:
    if score >= 0.68:
        return "High"
    if score >= 0.38:
        return "Medium"
    return "Low"
