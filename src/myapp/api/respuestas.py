from flask import Blueprint, jsonify

from myapp.api.request_data import json_object
from myapp.services import respuestas as service

api_respuestas_bp = Blueprint(
    "api_respuestas",
    __name__,
    url_prefix="/api/preguntas/<int:pregunta_id>/respuestas",
)


@api_respuestas_bp.get("")
def index(pregunta_id):
    respuestas = service.list_respuestas(pregunta_id)
    return jsonify([respuesta.to_dict() for respuesta in respuestas])


@api_respuestas_bp.post("")
def create(pregunta_id):
    respuesta = service.create_respuesta(pregunta_id, json_object())
    return respuesta.to_dict(), 201
