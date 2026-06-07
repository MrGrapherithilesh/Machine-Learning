import pandas as pd

from .model_trainer import FEATURES, load_models


def predict_customer_outcome(values):
    renewal_model, churn_model, scaler = load_models()
    row = pd.DataFrame([[values[field] for field in FEATURES]], columns=FEATURES)
    scaled_row = scaler.transform(row)

    renewal_probability = float(renewal_model.predict_proba(scaled_row)[0][1])
    churn_probability = float(churn_model.predict_proba(scaled_row)[0][1])

    return {
        "renewal_probability": round(renewal_probability * 100, 2),
        "churn_risk": round(churn_probability * 100, 2),
        "prediction_result": "Likely to Renew" if renewal_probability >= 0.55 else "Needs Follow-up",
        "risk_label": "High Churn Risk" if churn_probability >= 0.6 else "Manageable Risk",
    }


def forecast_revenue(current_revenue, growth_rate=0.08, months=6):
    forecast = []
    amount = current_revenue
    for month in range(1, months + 1):
        amount = amount * (1 + growth_rate)
        forecast.append({"month": month, "revenue": round(amount, 2)})
    return forecast
