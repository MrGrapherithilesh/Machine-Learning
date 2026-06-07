from datetime import datetime

from . import db


class Customer(db.Model):
    __tablename__ = "customers"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    phone = db.Column(db.String(25), nullable=False)
    company = db.Column(db.String(120), nullable=True)
    city = db.Column(db.String(80), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    subscriptions = db.relationship("Subscription", back_populates="customer", cascade="all, delete-orphan")
    invoices = db.relationship("Invoice", back_populates="customer", cascade="all, delete-orphan")
    payments = db.relationship("Payment", back_populates="customer", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Customer {self.name}>"
