import os


BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key-change-later")
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(BASE_DIR, "database", "billing_system.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TAX_RATE = 0.18
    DEFAULT_DISCOUNT = 0.05
