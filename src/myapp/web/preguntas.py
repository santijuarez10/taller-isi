from flask import Blueprint, flash, redirect, render_template, request, url_for

from myapp.services import preguntas as service
from myapp.services import respuestas as respuestas_service
from myapp.services import users as users_service
from myapp.services.errors import ValidationError

preguntas_bp = Blueprint("preguntas", __name__, url_prefix="/preguntas")


def _form(pregunta_id=None, data=None, errors=None, status=200):
    return (
        render_template(
            "preguntas/form.html",
            pregunta_id=pregunta_id,
            data=data or {},
            errors=errors or {},
            users=users_service.list_users(),
        ),
        status,
    )


def _detail(pregunta_id, data=None, errors=None, status=200):
    return (
        render_template(
            "preguntas/detail.html",
            pregunta=service.get_pregunta(pregunta_id),
            data=data or {},
            errors=errors or {},
            users=users_service.list_users(),
        ),
        status,
    )


@preguntas_bp.get("")
def index():
    return render_template("preguntas/index.html", preguntas=service.list_preguntas())


@preguntas_bp.get("/<int:pregunta_id>")
def detail(pregunta_id):
    return _detail(pregunta_id)


@preguntas_bp.get("/new")
def new():
    return _form()


@preguntas_bp.post("")
def create():
    try:
        pregunta = service.create_pregunta(request.form)
    except ValidationError as error:
        return _form(data=request.form, errors=error.errors, status=400)
    flash("Pregunta publicada")
    return redirect(url_for("preguntas.detail", pregunta_id=pregunta.id))


@preguntas_bp.get("/<int:pregunta_id>/edit")
def edit(pregunta_id):
    data = service.get_pregunta(pregunta_id).to_dict()
    data["tags"] = ", ".join(data["tags"])
    return _form(pregunta_id, data)


@preguntas_bp.post("/<int:pregunta_id>")
def update(pregunta_id):
    try:
        service.update_pregunta(pregunta_id, request.form)
    except ValidationError as error:
        return _form(pregunta_id, request.form, error.errors, 400)
    flash("Pregunta actualizada")
    return redirect(url_for("preguntas.detail", pregunta_id=pregunta_id))


@preguntas_bp.post("/<int:pregunta_id>/delete")
def delete(pregunta_id):
    service.delete_pregunta(pregunta_id)
    flash("Pregunta borrada")
    return redirect(url_for("preguntas.index"))


@preguntas_bp.post("/<int:pregunta_id>/respuestas")
def responder(pregunta_id):
    try:
        respuestas_service.create_respuesta(pregunta_id, request.form)
    except ValidationError as error:
        return _detail(pregunta_id, request.form, error.errors, 400)
    flash("Respuesta publicada")
    url = url_for("preguntas.detail", pregunta_id=pregunta_id)
    return redirect(f"{url}#respuestas")
