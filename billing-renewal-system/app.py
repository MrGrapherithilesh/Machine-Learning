from flask import Flask

from config import Config
from database.seed_data import seed_database
from ml.model_trainer import train_models
from models import db
from routes.customers import customers_bp
from routes.dashboard import dashboard_bp
from routes.invoices import invoices_bp
from routes.predictions import predictions_bp
from routes.renewals import renewals_bp
from routes.services import services_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    app.register_blueprint(dashboard_bp)
    app.register_blueprint(customers_bp)
    app.register_blueprint(services_bp)
    app.register_blueprint(invoices_bp)
    app.register_blueprint(renewals_bp)
    app.register_blueprint(predictions_bp)

    with app.app_context():
        db.create_all()
        seed_database()
        train_models()

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True)
