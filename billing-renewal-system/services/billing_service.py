from datetime import date, timedelta

from config import Config
from models import db
from models.invoice import Invoice
from models.payment import Payment


def calculate_invoice_amount(subtotal, discount_rate=None):
    discount_rate = Config.DEFAULT_DISCOUNT if discount_rate is None else discount_rate
    discount_amount = round(subtotal * discount_rate, 2)
    taxable_amount = subtotal - discount_amount
    tax_amount = round(taxable_amount * Config.TAX_RATE, 2)
    total_amount = round(taxable_amount + tax_amount, 2)
    return {
        "subtotal": round(subtotal, 2),
        "discount_amount": discount_amount,
        "tax_amount": tax_amount,
        "total_amount": total_amount,
    }


def next_invoice_number():
    latest = Invoice.query.order_by(Invoice.id.desc()).first()
    next_id = 1 if latest is None else latest.id + 1
    return f"INV-{date.today().year}-{next_id:04d}"


def create_invoice(customer_id, subscription, discount_rate=None):
    subtotal = subscription.service.price_for_plan(subscription.plan_type)
    values = calculate_invoice_amount(subtotal, discount_rate)
    invoice = Invoice(
        invoice_number=next_invoice_number(),
        customer_id=customer_id,
        subscription_id=subscription.id,
        issue_date=date.today(),
        due_date=date.today() + timedelta(days=10),
        status="Unpaid",
        **values,
    )
    db.session.add(invoice)
    db.session.commit()
    return invoice


def record_payment(invoice, amount, payment_mode, reference_number=""):
    payment = Payment(
        invoice_id=invoice.id,
        customer_id=invoice.customer_id,
        amount=amount,
        payment_date=date.today(),
        payment_mode=payment_mode,
        reference_number=reference_number,
    )
    invoice.status = "Paid" if amount >= invoice.total_amount else "Partial"
    db.session.add(payment)
    db.session.commit()
    return payment
