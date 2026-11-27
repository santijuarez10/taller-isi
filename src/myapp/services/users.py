import logging

from sqlalchemy.exc import IntegrityError

from myapp.extensions import db
from myapp.models import User
from myapp.services.errors import ConflictError, NotFoundError, ValidationError
from myapp.services.validation import clean_text

logger = logging.getLogger(__name__)

FIELDS = ("name", "email")


def list_users():
    return db.session.scalars(db.select(User).order_by(User.name, User.id)).all()


def get_user(user_id):
    user = db.session.get(User, user_id)
    if user is None:
        raise NotFoundError("Usuario no encontrado")
    return user


def _validate(data):
    errors = {}
    name = clean_text(data, "name", errors, 120)
    email = clean_text(data, "email", errors, 255).lower()
    if "email" not in errors:
        local, _, domain = email.partition("@")
        if not local or not domain or " " in email or "@" in domain:
            errors["email"] = "No es un email válido"
    if errors:
        raise ValidationError(errors)
    return {"name": name, "email": email}


def _commit():
    try:
        db.session.commit()
    except IntegrityError as error:
        db.session.rollback()
        raise ConflictError("Ya existe un usuario con ese email") from error


def create_user(data):
    user = User(**_validate(data))
    db.session.add(user)
    _commit()
    logger.info("Usuario creado id=%s", user.id)
    return user


def update_user(user_id, data):
    """Actualiza los campos presentes en data; el resto queda igual."""
    user = get_user(user_id)
    current = {field: getattr(user, field) for field in FIELDS}
    changes = {field: data[field] for field in FIELDS if field in data}
    for field, value in _validate(current | changes).items():
        setattr(user, field, value)
    _commit()
    logger.info("Usuario actualizado id=%s", user.id)
    return user


def delete_user(user_id):
    user = get_user(user_id)
    if user.preguntas or user.respuestas:
        raise ConflictError(
            "No se puede borrar un usuario que tiene preguntas o respuestas"
        )
    db.session.delete(user)
    db.session.commit()
    logger.info("Usuario borrado id=%s", user_id)
