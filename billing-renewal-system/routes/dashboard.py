from flask import Blueprint, render_template

from models.payment import Payment
from models.subscription import Subscription
from services.dashboard_service import dashboard_stats, monthly_revenue_data
from services.renewal_service import upcoming_renewals


dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/")
def index():
    stats = dashboard_stats()
    recent_payments = Payment.query.order_by(Payment.payment_date.desc()).limit(5).all()
    expiring = upcoming_renewals(30)
    active = Subscription.query.filter_by(status="Active").limit(5).all()
    return render_template(
        "dashboard.html",
        stats=stats,
        chart_data=monthly_revenue_data(),
        recent_payments=recent_payments,
        expiring=expiring,
        active=active,
    )
