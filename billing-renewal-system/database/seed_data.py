from datetime import date, timedelta

from models import db
from models.customer import Customer
from models.invoice import Invoice
from models.payment import Payment
from models.renewal import Renewal
from models.service import Service
from models.subscription import Subscription
from services.billing_service import calculate_invoice_amount


def seed_database():
    if Customer.query.first():
        return

    services = [
        Service(
            name="Cloud Backup",
            description="Storage and backup plan for small teams",
            monthly_price=999,
            quarterly_price=2799,
            yearly_price=9999,
        ),
        Service(
            name="CRM Starter",
            description="Simple customer relationship dashboard",
            monthly_price=1499,
            quarterly_price=4199,
            yearly_price=14999,
        ),
        Service(
            name="Analytics Pro",
            description="Business reports and monthly analytics",
            monthly_price=2499,
            quarterly_price=6999,
            yearly_price=24999,
        ),
    ]
    db.session.add_all(services)
    db.session.flush()

    customers = [
        Customer(name="Aarav Sharma", email="aarav@example.com", phone="9876543210", company="Northbyte Labs", city="Pune"),
        Customer(name="Nisha Rao", email="nisha@example.com", phone="9876501234", company="FreshKart", city="Hyderabad"),
        Customer(name="Rohan Mehta", email="rohan@example.com", phone="9988776655", company="EduTrail", city="Bengaluru"),
        Customer(name="Priya Nair", email="priya@example.com", phone="9123456780", company="PixelDesk", city="Kochi"),
    ]
    db.session.add_all(customers)
    db.session.flush()

    today = date.today()
    subscriptions = [
        Subscription(customer_id=customers[0].id, service_id=services[0].id, plan_type="Yearly", start_date=today - timedelta(days=320), end_date=today + timedelta(days=45), status="Active"),
        Subscription(customer_id=customers[1].id, service_id=services[1].id, plan_type="Quarterly", start_date=today - timedelta(days=70), end_date=today + timedelta(days=20), status="Active"),
        Subscription(customer_id=customers[2].id, service_id=services[2].id, plan_type="Monthly", start_date=today - timedelta(days=35), end_date=today - timedelta(days=5), status="Expired"),
        Subscription(customer_id=customers[3].id, service_id=services[1].id, plan_type="Monthly", start_date=today - timedelta(days=12), end_date=today + timedelta(days=18), status="Active"),
    ]
    db.session.add_all(subscriptions)
    db.session.flush()

    invoices = []
    for index, subscription in enumerate(subscriptions, start=1):
        service = Service.query.get(subscription.service_id)
        values = calculate_invoice_amount(service.price_for_plan(subscription.plan_type))
        invoice = Invoice(
            invoice_number=f"INV-{today.year}-{index:04d}",
            customer_id=subscription.customer_id,
            subscription_id=subscription.id,
            issue_date=today - timedelta(days=10 + index),
            due_date=today + timedelta(days=5 + index),
            status="Paid" if index <= 3 else "Unpaid",
            **values,
        )
        invoices.append(invoice)
    db.session.add_all(invoices)
    db.session.flush()

    payments = [
        Payment(invoice_id=invoices[0].id, customer_id=invoices[0].customer_id, amount=invoices[0].total_amount, payment_date=today - timedelta(days=25), payment_mode="UPI", reference_number="UPI1001"),
        Payment(invoice_id=invoices[1].id, customer_id=invoices[1].customer_id, amount=invoices[1].total_amount, payment_date=today - timedelta(days=16), payment_mode="Card", reference_number="CARD4421"),
        Payment(invoice_id=invoices[2].id, customer_id=invoices[2].customer_id, amount=invoices[2].total_amount, payment_date=today - timedelta(days=7), payment_mode="Bank Transfer", reference_number="NEFT2310"),
    ]
    reminders = [
        Renewal(subscription_id=subscriptions[1].id, reminder_date=today + timedelta(days=13), renewal_status="Pending", notes="Send reminder email this week"),
        Renewal(subscription_id=subscriptions[2].id, reminder_date=today - timedelta(days=3), renewal_status="Expired", notes="Call customer for reactivation"),
    ]
    db.session.add_all(payments + reminders)
    db.session.commit()
