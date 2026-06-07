from datetime import datetime

from . import db


class Subscription(db.Model):
    __tablename__ = "subscriptions"

    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey("customers.id"), nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey("services.id"), nullable=False)
    plan_type = db.Column(db.String(20), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(20), default="Active")
    auto_renew = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    customer = db.relationship("Customer", back_populates="subscriptions")
    service = db.relationship("Service", back_populates="subscriptions")
    invoices = db.relationship("Invoice", back_populates="subscription")
    renewals = db.relationship("Renewal", back_populates="subscription", cascade="all, delete-orphan")

    def days_left(self, today=None):
        today = today or datetime.utcnow().date()
        return (self.end_date - today).days

    def __repr__(self):
        return f"<Subscription {self.customer_id}-{self.service_id}>"
