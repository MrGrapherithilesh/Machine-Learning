from datetime import datetime

from . import db


class Payment(db.Model):
    __tablename__ = "payments"

    id = db.Column(db.Integer, primary_key=True)
    invoice_id = db.Column(db.Integer, db.ForeignKey("invoices.id"), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey("customers.id"), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    payment_date = db.Column(db.Date, nullable=False)
    payment_mode = db.Column(db.String(40), nullable=False)
    reference_number = db.Column(db.String(80), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    invoice = db.relationship("Invoice", back_populates="payments")
    customer = db.relationship("Customer", back_populates="payments")

    def __repr__(self):
        return f"<Payment {self.amount}>"
