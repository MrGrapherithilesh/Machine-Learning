from datetime import datetime

from . import db


class Renewal(db.Model):
    __tablename__ = "renewals"

    id = db.Column(db.Integer, primary_key=True)
    subscription_id = db.Column(db.Integer, db.ForeignKey("subscriptions.id"), nullable=False)
    reminder_date = db.Column(db.Date, nullable=False)
    renewal_status = db.Column(db.String(30), default="Pending")
    notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    subscription = db.relationship("Subscription", back_populates="renewals")

    def __repr__(self):
        return f"<Renewal {self.subscription_id}>"
