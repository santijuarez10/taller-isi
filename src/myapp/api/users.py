from flask import Blueprint, jsonify, url_for

from myapp.api.request_data import json_object
from myapp.services import users as service

api_users_bp = Blueprint("api_users", __name__, url_prefix="/api/users")


@api_users_bp.get("")
def index():
    return jsonify([user.to_dict() for user in service.list_users()])


@api_users_bp.get("/<int:user_id>")
def detail(user_id):
    return service.get_user(user_id).to_dict()


@api_users_bp.post("")
def create():
    user = service.create_user(json_object())
    location = url_for("api_users.detail", user_id=user.id)
    return user.to_dict(), 201, {"Location": location}


@api_users_bp.patch("/<int:user_id>")
def update(user_id):
    return service.update_user(user_id, json_object()).to_dict()


@api_users_bp.delete("/<int:user_id>")
def delete(user_id):
    service.delete_user(user_id)
    return "", 204
