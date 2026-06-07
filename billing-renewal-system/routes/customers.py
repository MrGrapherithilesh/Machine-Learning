from datetime import date, timedelta

from flask import Blueprint, flash, redirect, render_template, request, url_for

from models import db
from models.customer import Customer
from models.service import Service
from models.subscription import Subscription


customers_bp = Blueprint("customers", __name__, url_prefix="/customers")


@customers_bp.route("/")
def list_customers():
    query = request.args.get("q", "").strip()
    customers = Customer.query
    if query:
        search_text = f"%{query}%"
        customers = customers.filter(
            (Customer.name.ilike(search_text))
            | (Customer.email.ilike(search_text))
            | (Customer.company.ilike(search_text))
        )
    return render_template("customers.html", customers=customers.order_by(Customer.created_at.desc()).all(), query=query)


@customers_bp.route("/add", methods=["GET", "POST"])
def add_customer():
    if request.method == "POST":
        customer = Customer(
            name=request.form["name"].strip(),
            email=request.form["email"].strip().lower(),
            phone=request.form["phone"].strip(),
            company=request.form.get("company", "").strip(),
            city=request.form.get("city", "").strip(),
        )
        db.session.add(customer)
        db.session.commit()
        flash("Customer added successfully.", "success")
        return redirect(url_for("customers.view_customer", customer_id=customer.id))
    return render_template("customer_form.html", customer=None)


@customers_bp.route("/<int:customer_id>")
def view_customer(customer_id):
    customer = Customer.query.get_or_404(customer_id)
    services = Service.query.filter_by(is_active=True).all()
    return render_template("customer_profile.html", customer=customer, services=services)


@customers_bp.route("/<int:customer_id>/edit", methods=["GET", "POST"])
def edit_customer(customer_id):
    customer = Customer.query.get_or_404(customer_id)
    if request.method == "POST":
        customer.name = request.form["name"].strip()
        customer.email = request.form["email"].strip().lower()
        customer.phone = request.form["phone"].strip()
        customer.company = request.form.get("company", "").strip()
        customer.city = request.form.get("city", "").strip()
        db.session.commit()
        flash("Customer details updated.", "success")
        return redirect(url_for("customers.view_customer", customer_id=customer.id))
    return render_template("customer_form.html", customer=customer)


@customers_bp.route("/<int:customer_id>/delete", methods=["POST"])
def delete_customer(customer_id):
    customer = Customer.query.get_or_404(customer_id)
    db.session.delete(customer)
    db.session.commit()
    flash("Customer deleted.", "info")
    return redirect(url_for("customers.list_customers"))


@customers_bp.route("/<int:customer_id>/subscribe", methods=["POST"])
def add_subscription(customer_id):
    service = Service.query.get_or_404(int(request.form["service_id"]))
    plan_type = request.form["plan_type"]
    start_date = date.today()
    plan_days = {"Monthly": 30, "Quarterly": 90, "Yearly": 365}
    subscription = Subscription(
        customer_id=customer_id,
        service_id=service.id,
        plan_type=plan_type,
        start_date=start_date,
        end_date=start_date + timedelta(days=plan_days[plan_type]),
        status="Active",
        auto_renew=bool(request.form.get("auto_renew")),
    )
    db.session.add(subscription)
    db.session.commit()
    flash("Subscription added for customer.", "success")
    return redirect(url_for("customers.view_customer", customer_id=customer_id))
