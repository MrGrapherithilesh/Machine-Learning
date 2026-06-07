from datetime import datetime

from . import db


class Service(db.Model):
    __tablename__ = "services"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=True)
    monthly_price = db.Column(db.Float, nullable=False)
    quarterly_price = db.Column(db.Float, nullable=False)
    yearly_price = db.Column(db.Float, nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    subscriptions = db.relationship("Subscription", back_populates="service")

    def price_for_plan(self, plan_type):
        if plan_type == "Monthly":
            return self.monthly_price
        if plan_type == "Quarterly":
            return self.quarterly_price
        return self.yearly_price

    def __repr__(self):
        return f"<Service {self.name}>"
