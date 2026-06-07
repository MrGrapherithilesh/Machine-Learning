import os

import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler


BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATASET_PATH = os.path.join(BASE_DIR, "sample_subscription_data.csv")
RENEWAL_MODEL_PATH = os.path.join(BASE_DIR, "renewal_model.pkl")
CHURN_MODEL_PATH = os.path.join(BASE_DIR, "churn_model.pkl")
SCALER_PATH = os.path.join(BASE_DIR, "scaler.pkl")


FEATURES = [
    "months_active",
    "monthly_spend",
    "support_tickets",
    "late_payments",
    "usage_score",
    "previous_renewals",
]


def create_sample_dataset():
    np.random.seed(42)
    rows = 180
    data = pd.DataFrame(
        {
            "months_active": np.random.randint(1, 48, rows),
            "monthly_spend": np.random.randint(799, 12999, rows),
            "support_tickets": np.random.randint(0, 8, rows),
            "late_payments": np.random.randint(0, 6, rows),
            "usage_score": np.random.randint(20, 100, rows),
            "previous_renewals": np.random.randint(0, 6, rows),
        }
    )

    renewal_signal = (
        data["usage_score"] * 0.03
        + data["previous_renewals"] * 0.45
        + data["months_active"] * 0.02
        - data["late_payments"] * 0.35
        - data["support_tickets"] * 0.08
    )
    churn_signal = (
        data["late_payments"] * 0.5
        + data["support_tickets"] * 0.25
        - data["usage_score"] * 0.025
        - data["previous_renewals"] * 0.35
    )

    data["renewed"] = (renewal_signal > renewal_signal.median()).astype(int)
    data["churned"] = (churn_signal > churn_signal.median()).astype(int)
    data.to_csv(DATASET_PATH, index=False)
    return data


def load_dataset():
    if not os.path.exists(DATASET_PATH):
        return create_sample_dataset()
    return pd.read_csv(DATASET_PATH)


def train_models():
    data = load_dataset()
    x = data[FEATURES]
    y_renewal = data["renewed"]
    y_churn = data["churned"]

    scaler = StandardScaler()
    x_scaled = scaler.fit_transform(x)

    x_train, _, renewal_train, _ = train_test_split(x_scaled, y_renewal, test_size=0.2, random_state=21)
    x_churn_train, _, churn_train, _ = train_test_split(x_scaled, y_churn, test_size=0.2, random_state=21)

    renewal_model = RandomForestClassifier(n_estimators=90, random_state=21)
    churn_model = LogisticRegression(max_iter=500)

    renewal_model.fit(x_train, renewal_train)
    churn_model.fit(x_churn_train, churn_train)

    joblib.dump(renewal_model, RENEWAL_MODEL_PATH)
    joblib.dump(churn_model, CHURN_MODEL_PATH)
    joblib.dump(scaler, SCALER_PATH)
    return renewal_model, churn_model, scaler


def load_models():
    if not all(os.path.exists(path) for path in [RENEWAL_MODEL_PATH, CHURN_MODEL_PATH, SCALER_PATH]):
        return train_models()
    return joblib.load(RENEWAL_MODEL_PATH), joblib.load(CHURN_MODEL_PATH), joblib.load(SCALER_PATH)
