from flask import Blueprint, render_template

users_bp = Blueprint("users", __name__, url_prefix="/users")


@users_bp.get("/")
def index():
    users = [
        {"name": "Ada Lovelace", "email": "ada@example.com"},
        {"name": "Alan Turing", "email": "alan@example.com"},
    ]

    return render_template("users/index.html", users=users)