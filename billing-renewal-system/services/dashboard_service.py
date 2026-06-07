from datetime import date, timedelta

from sqlalchemy import func

from models.customer import Customer
from models.invoice import Invoice
from models.payment import Payment
from models.subscription import Subscription


def dashboard_stats():
    today = date.today()
    month_start = today.replace(day=1)
    next_month = month_start + timedelta(days=32)
    next_month = next_month.replace(day=1)

    total_customers = Customer.query.count()
    active_subscriptions = Subscription.query.filter(Subscription.status == "Active").count()
    expiring_subscriptions = (
        Subscription.query.filter(Subscription.end_date >= today)
        .filter(Subscription.end_date <= today + timedelta(days=30))
        .count()
    )
    monthly_revenue = (
        Payment.query.filter(Payment.payment_date >= month_start)
        .filter(Payment.payment_date < next_month)
        .with_entities(func.coalesce(func.sum(Payment.amount), 0))
        .scalar()
    )
    unpaid_invoices = Invoice.query.filter(Invoice.status != "Paid").count()

    return {
        "total_customers": total_customers,
        "active_subscriptions": active_subscriptions,
        "expiring_subscriptions": expiring_subscriptions,
        "monthly_revenue": monthly_revenue,
        "unpaid_invoices": unpaid_invoices,
    }


def monthly_revenue_data():
    rows = (
        Payment.query.with_entities(
            func.strftime("%Y-%m", Payment.payment_date).label("month"),
            func.sum(Payment.amount).label("revenue"),
        )
        .group_by("month")
        .order_by("month")
        .all()
    )
    return {
        "labels": [row.month for row in rows][-6:],
        "values": [round(row.revenue or 0, 2) for row in rows][-6:],
    }
