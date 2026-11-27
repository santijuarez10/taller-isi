import os

from dotenv import find_dotenv, load_dotenv

# Carga .env (si existe) sin pisar las variables que ya estén definidas.
load_dotenv(find_dotenv(usecwd=True))

DEFAULT_SECRET_KEY = "development-only-key"


class Config:
    APP_ENV = os.getenv("APP_ENV", "development")
    SECRET_KEY = os.getenv("SECRET_KEY", DEFAULT_SECRET_KEY)
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///app.db")
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")


class TestingConfig(Config):
    APP_ENV = "testing"
    TESTING = True
    SECRET_KEY = "testing-key"
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
