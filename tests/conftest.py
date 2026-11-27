import pytest

from myapp import create_app
from myapp.config import TestingConfig
from myapp.extensions import db


@pytest.fixture
def app():
    # La configuración se pasa ANTES de crear la app: así los tests usan
    # una base en memoria y nunca tocan la base de desarrollo.
    app = create_app(TestingConfig)

    with app.app_context():
        db.create_all()

    yield app

    with app.app_context():
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def user_id(client):
    response = client.post(
        "/api/users", json={"name": "Ada Lovelace", "email": "ada@example.com"}
    )
    return response.json["id"]


@pytest.fixture
def pregunta_data(user_id):
    return {
        "titulo": "¿Qué es un Blueprint?",
        "cuerpo": "No entiendo para qué sirve.",
        "autor_id": user_id,
        "categoria": "Flask",
        "tags": ["python", "web"],
    }
