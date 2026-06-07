# Billing & Subscription Renewal Management System

This is a Flask based Billing and Subscription Renewal Management System built by Mithilesh as a personal portfolio project. The app handles customers, subscription services, invoices, payments, renewals, and basic prediction workflows for renewal and churn analysis.

## Project Overview

BillingFlow is a small business style web app for tracking subscription customers and their billing cycle. It has customer management, service plans, invoice generation, payment tracking, renewal reminders, dashboard analytics, and a machine learning page for renewal probability and churn risk.

The project uses SQLite so it can run easily on a laptop without extra setup. When the app starts for the first time, it creates the database, adds sample records, creates a sample dataset, and trains the prediction models.

## Motivation

I built this project to understand how billing systems, subscription management, and machine learning can be integrated into a real-world application. As an AIML student, I wanted to combine software development with predictive analytics.

I started with a simple billing idea and slowly expanded it into subscription tracking, renewal reminders, dashboards, and prediction features. It helped me connect backend development, database design, UI work, and ML concepts in one project.

## Features

- Add, edit, delete, search, and view customer profiles
- Manage subscription services with monthly, quarterly, and yearly plans
- Assign subscriptions to customers
- Generate invoices from active subscriptions
- Calculate subtotal, discount, tax, and final amount
- Track paid, unpaid, and partial payments
- View upcoming renewals and expired subscriptions
- Add renewal reminders and generate renewal invoices
- Dashboard with customer count, active plans, expiring plans, unpaid invoices, and revenue
- Monthly revenue chart for portfolio screenshots
- Renewal prediction using Random Forest Classifier
- Churn prediction using Logistic Regression
- Revenue forecasting for the next few months
- Responsive Bootstrap UI with a clean white and blue theme

## Technologies Used

- Python
- Flask
- SQLAlchemy
- SQLite
- HTML
- CSS
- Bootstrap
- JavaScript
- Chart.js
- Pandas
- NumPy
- Scikit-learn

## Project Structure

```text
billing-renewal-system/
├── app.py
├── config.py
├── requirements.txt
├── README.md
├── DEVELOPMENT_PLAN.md
├── models/
├── routes/
├── services/
├── ml/
├── static/
├── templates/
├── database/
└── screenshots/
```

## Installation Steps

1. Clone the project or download the folder.

2. Move into the project directory.

```bash
cd billing-renewal-system
```

3. Create and activate a virtual environment.

```bash
python -m venv venv
source venv/bin/activate
```

On Windows:

```bash
venv\Scripts\activate
```

4. Install dependencies.

```bash
pip install -r requirements.txt
```

5. Run the Flask app.

```bash
python app.py
```

6. Open the app in browser.

```text
http://127.0.0.1:5000
```

## Screenshots Section

Screenshots can be added inside the `screenshots/` folder after running the app locally.

Suggested screenshots:

- Dashboard page
- Customer management page
- Customer profile page
- Invoice history page
- Renewal management page
- Prediction page

## Development Journey

This project started as a basic customer and invoice tracking idea. In the first version, I focused on the Flask setup, database connection, and customer records. After that, I added services and subscription plans because billing only makes sense when the customer is linked to a service.

The next part was invoice generation. I added tax and discount calculations, then payment tracking so invoice status could be updated properly. Once the billing flow was working, I added renewal management because subscription based apps need reminders for expiring plans.

Later, I improved the dashboard with revenue cards, recent payments, upcoming renewals, and a chart. The final major step was the machine learning module. I created a sample subscription dataset and trained two models: one for renewal prediction and one for churn prediction. This made the project feel closer to an AIML portfolio project instead of only a CRUD web app.

## Future Improvements

- Add user login and role based access
- Add email reminders for renewal follow-ups
- Export invoices as PDF files
- Add more detailed revenue reports
- Add filters for invoice and payment history
- Improve the ML dataset with real business features
- Add unit tests for billing calculations

## Learning Outcomes

- Designed a relational database for customers, subscriptions, invoices, payments, and renewals
- Practiced Flask routing and SQLAlchemy relationships
- Built a clean Bootstrap based dashboard
- Implemented billing calculations with tax and discounts
- Connected a simple ML workflow with a web application
- Learned how subscription renewal and churn prediction can support business decisions

## Author

Mithilesh

B.Tech AIML Student
