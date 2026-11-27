from flask import Blueprint, flash, redirect, render_template, request, url_for

from myapp.services import users as service
from myapp.services.errors import ConflictError, ValidationError

users_bp = Blueprint("users", __name__, url_prefix="/users")


def _form(user_id=None, data=None, errors=None, status=200):
    return (
        render_template(
            "users/form.html",
            user_id=user_id,
            data=data or {},
            errors=errors or {},
        ),
        status,
    )


@users_bp.get("")
def index():
    return render_template("users/index.html", users=service.list_users())


@users_bp.get("/<int:user_id>")
def detail(user_id):
    return render_template("users/detail.html", user=service.get_user(user_id))


@users_bp.get("/new")
def new():
    return _form()


@users_bp.post("")
def create():
    try:
        user = service.create_user(request.form)
    except ValidationError as error:
        return _form(data=request.form, errors=error.errors, status=400)
    except ConflictError as error:
        return _form(data=request.form, errors={"email": str(error)}, status=409)
    flash("Usuario creado")
    return redirect(url_for("users.detail", user_id=user.id))


@users_bp.get("/<int:user_id>/edit")
def edit(user_id):
    return _form(user_id, service.get_user(user_id).to_dict())


@users_bp.post("/<int:user_id>")
def update(user_id):
    try:
        service.update_user(user_id, request.form)
    except ValidationError as error:
        return _form(user_id, request.form, error.errors, 400)
    except ConflictError as error:
        return _form(user_id, request.form, {"email": str(error)}, 409)
    flash("Usuario actualizado")
    return redirect(url_for("users.detail", user_id=user_id))


@users_bp.post("/<int:user_id>/delete")
def delete(user_id):
    try:
        service.delete_user(user_id)
    except ConflictError as error:
        flash(str(error))
        return redirect(url_for("users.detail", user_id=user_id))
    flash("Usuario borrado")
    return redirect(url_for("users.index"))
