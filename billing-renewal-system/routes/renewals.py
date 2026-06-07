from datetime import date, timedelta

from flask import Blueprint, flash, redirect, render_template, request, url_for

from models import db
from models.subscription import Subscription
from services.billing_service import create_invoice
from services.renewal_service import create_renewal_reminder, expired_subscriptions, subscription_status, upcoming_renewals


renewals_bp = Blueprint("renewals", __name__, url_prefix="/renewals")


@renewals_bp.route("/")
def renewal_center():
    subscriptions = Subscription.query.order_by(Subscription.end_date.asc()).all()
    return render_template(
        "renewals.html",
        subscriptions=subscriptions,
        upcoming=upcoming_renewals(30),
        expired=expired_subscriptions(),
        status_for=subscription_status,
    )


@renewals_bp.route("/<int:subscription_id>/remind", methods=["POST"])
def add_reminder(subscription_id):
    subscription = Subscription.query.get_or_404(subscription_id)
    create_renewal_reminder(subscription, request.form.get("notes", "").strip())
    flash("Renewal reminder created.", "success")
    return redirect(url_for("renewals.renewal_center"))


@renewals_bp.route("/<int:subscription_id>/renew", methods=["POST"])
def renew_subscription(subscription_id):
    subscription = Subscription.query.get_or_404(subscription_id)
    plan_days = {"Monthly": 30, "Quarterly": 90, "Yearly": 365}
    start = max(date.today(), subscription.end_date)
    subscription.start_date = start
    subscription.end_date = start + timedelta(days=plan_days[subscription.plan_type])
    subscription.status = "Active"
    db.session.commit()
    invoice = create_invoice(subscription.customer_id, subscription)
    flash(f"Subscription renewed and {invoice.invoice_number} generated.", "success")
    return redirect(url_for("renewals.renewal_center"))
