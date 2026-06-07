from flask import Blueprint, render_template, request

from ml.predictor import forecast_revenue, predict_customer_outcome
from models.payment import Payment


predictions_bp = Blueprint("predictions", __name__, url_prefix="/predictions")


@predictions_bp.route("/", methods=["GET", "POST"])
def prediction_page():
    result = None
    values = {
        "months_active": 14,
        "monthly_spend": 2499,
        "support_tickets": 2,
        "late_payments": 1,
        "usage_score": 78,
        "previous_renewals": 2,
    }
    if request.method == "POST":
        values = {key: float(request.form[key]) for key in values}
        result = predict_customer_outcome(values)

    current_revenue = sum(payment.amount for payment in Payment.query.all()) or 25000
    revenue_forecast = forecast_revenue(current_revenue)
    return render_template("predictions.html", result=result, values=values, revenue_forecast=revenue_forecast)
