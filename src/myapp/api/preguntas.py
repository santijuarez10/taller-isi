from flask import Blueprint, jsonify, url_for

from myapp.api.request_data import json_object
from myapp.services import preguntas as service

api_preguntas_bp = Blueprint("api_preguntas", __name__, url_prefix="/api/preguntas")


@api_preguntas_bp.get("")
def index():
    return jsonify([pregunta.to_dict() for pregunta in service.list_preguntas()])


@api_preguntas_bp.get("/<int:pregunta_id>")
def detail(pregunta_id):
    return service.get_pregunta(pregunta_id).to_dict()


@api_preguntas_bp.post("")
def create():
    pregunta = service.create_pregunta(json_object())
    location = url_for("api_preguntas.detail", pregunta_id=pregunta.id)
    return pregunta.to_dict(), 201, {"Location": location}


@api_preguntas_bp.patch("/<int:pregunta_id>")
def update(pregunta_id):
    return service.update_pregunta(pregunta_id, json_object()).to_dict()


@api_preguntas_bp.delete("/<int:pregunta_id>")
def delete(pregunta_id):
    service.delete_pregunta(pregunta_id)
    return "", 204
