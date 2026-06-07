from datetime import date, timedelta

from models import db
from models.renewal import Renewal
from models.subscription import Subscription


def subscription_status(subscription):
    days = subscription.days_left(date.today())
    if days < 0:
        return "Expired"
    if days <= 15:
        return "Expiring Soon"
    return "Active"


def upcoming_renewals(days=30):
    today = date.today()
    limit = today + timedelta(days=days)
    return (
        Subscription.query.filter(Subscription.end_date >= today)
        .filter(Subscription.end_date <= limit)
        .order_by(Subscription.end_date.asc())
        .all()
    )


def expired_subscriptions():
    return Subscription.query.filter(Subscription.end_date < date.today()).order_by(Subscription.end_date.asc()).all()


def create_renewal_reminder(subscription, notes=""):
    reminder = Renewal(
        subscription_id=subscription.id,
        reminder_date=max(date.today(), subscription.end_date - timedelta(days=7)),
        renewal_status="Pending",
        notes=notes,
    )
    db.session.add(reminder)
    db.session.commit()
    return reminder
