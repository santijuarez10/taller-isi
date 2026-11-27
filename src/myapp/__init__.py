import logging
import sys

from flask import Flask, jsonify, redirect, render_template, request, url_for
from werkzeug.exceptions import HTTPException

from myapp.config import DEFAULT_SECRET_KEY, Config
from myapp.extensions import db


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    unsafe_keys = {DEFAULT_SECRET_KEY, "change-me", ""}
    if app.config["APP_ENV"] == "production" and (
        app.config["SECRET_KEY"] in unsafe_keys
    ):
        raise RuntimeError("En producción hay que definir un SECRET_KEY propio")

    logging.basicConfig(
        stream=sys.stdout,
        level=app.config["LOG_LEVEL"],
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )

    # /users y /users/ responden lo mismo.
    app.url_map.strict_slashes = False

    db.init_app(app)

    from myapp import models  # noqa: F401  (registra las tablas)
    from myapp.api.health import health_bp
    from myapp.api.preguntas import api_preguntas_bp
    from myapp.api.respuestas import api_respuestas_bp
    from myapp.api.users import api_users_bp
    from myapp.web.preguntas import preguntas_bp
    from myapp.web.users import users_bp

    for blueprint in (
        health_bp,
        users_bp,
        preguntas_bp,
        api_users_bp,
        api_preguntas_bp,
        api_respuestas_bp,
    ):
        app.register_blueprint(blueprint)

    @app.get("/")
    def home():
        return redirect(url_for("preguntas.index"))

    register_error_handlers(app)

    return app


def register_error_handlers(app):
    from myapp.services.errors import ConflictError, NotFoundError, ValidationError

    def respond(status, message, details=None):
        if request.path.startswith("/api/"):
            body = {"error": message}
            if details:
                body["details"] = details
            return jsonify(body), status
        return render_template("errors/error.html", message=message), status

    @app.errorhandler(NotFoundError)
    def not_found(error):
        return respond(404, str(error))

    @app.errorhandler(ConflictError)
    def conflict(error):
        return respond(409, str(error))

    @app.errorhandler(ValidationError)
    def invalid(error):
        return respond(400, "Datos inválidos", error.errors)

    @app.errorhandler(HTTPException)
    def http_error(error):
        if error.code and error.code < 400:
            return error
        messages = {
            404: "Página no encontrada",
            405: "Método no permitido",
        }
        return respond(error.code, messages.get(error.code, error.name))
