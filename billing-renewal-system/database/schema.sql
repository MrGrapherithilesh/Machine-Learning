CREATE TABLE customers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(120) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    phone VARCHAR(25) NOT NULL,
    company VARCHAR(120),
    city VARCHAR(80),
    created_at DATETIME
);

CREATE TABLE services (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(120) NOT NULL,
    description TEXT,
    monthly_price FLOAT NOT NULL,
    quarterly_price FLOAT NOT NULL,
    yearly_price FLOAT NOT NULL,
    is_active BOOLEAN,
    created_at DATETIME
);

CREATE TABLE subscriptions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER NOT NULL,
    service_id INTEGER NOT NULL,
    plan_type VARCHAR(20) NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    status VARCHAR(20),
    auto_renew BOOLEAN,
    created_at DATETIME,
    FOREIGN KEY(customer_id) REFERENCES customers(id),
    FOREIGN KEY(service_id) REFERENCES services(id)
);

CREATE TABLE invoices (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    invoice_number VARCHAR(30) NOT NULL UNIQUE,
    customer_id INTEGER NOT NULL,
    subscription_id INTEGER,
    issue_date DATE NOT NULL,
    due_date DATE NOT NULL,
    subtotal FLOAT NOT NULL,
    tax_amount FLOAT NOT NULL,
    discount_amount FLOAT NOT NULL,
    total_amount FLOAT NOT NULL,
    status VARCHAR(20),
    created_at DATETIME,
    FOREIGN KEY(customer_id) REFERENCES customers(id),
    FOREIGN KEY(subscription_id) REFERENCES subscriptions(id)
);

CREATE TABLE payments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    invoice_id INTEGER NOT NULL,
    customer_id INTEGER NOT NULL,
    amount FLOAT NOT NULL,
    payment_date DATE NOT NULL,
    payment_mode VARCHAR(40) NOT NULL,
    reference_number VARCHAR(80),
    created_at DATETIME,
    FOREIGN KEY(invoice_id) REFERENCES invoices(id),
    FOREIGN KEY(customer_id) REFERENCES customers(id)
);

CREATE TABLE renewals (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    subscription_id INTEGER NOT NULL,
    reminder_date DATE NOT NULL,
    renewal_status VARCHAR(30),
    notes TEXT,
    created_at DATETIME,
    FOREIGN KEY(subscription_id) REFERENCES subscriptions(id)
);
