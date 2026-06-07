from flask import Blueprint, flash, redirect, render_template, request, url_for

from models.customer import Customer
from models.invoice import Invoice
from models.subscription import Subscription
from services.billing_service import create_invoice, record_payment


invoices_bp = Blueprint("invoices", __name__, url_prefix="/invoices")


@invoices_bp.route("/")
def invoice_history():
    invoices = Invoice.query.order_by(Invoice.issue_date.desc()).all()
    subscriptions = Subscription.query.order_by(Subscription.created_at.desc()).all()
    return render_template("invoices.html", invoices=invoices, subscriptions=subscriptions)


@invoices_bp.route("/generate", methods=["POST"])
def generate_invoice():
    subscription = Subscription.query.get_or_404(int(request.form["subscription_id"]))
    invoice = create_invoice(subscription.customer_id, subscription)
    flash(f"Invoice {invoice.invoice_number} generated.", "success")
    return redirect(url_for("invoices.invoice_history"))


@invoices_bp.route("/<int:invoice_id>/pay", methods=["POST"])
def mark_payment():
    invoice = Invoice.query.get_or_404(invoice_id)
    amount = float(request.form.get("amount") or invoice.total_amount)
    mode = request.form.get("payment_mode", "UPI")
    reference_number = request.form.get("reference_number", "").strip()
    record_payment(invoice, amount, mode, reference_number)
    flash("Payment recorded.", "success")
    return redirect(url_for("invoices.invoice_history"))


@invoices_bp.route("/new")
def new_invoice():
    customers = Customer.query.order_by(Customer.name.asc()).all()
    subscriptions = Subscription.query.order_by(Subscription.created_at.desc()).all()
    return render_template("invoice_form.html", customers=customers, subscriptions=subscriptions)
