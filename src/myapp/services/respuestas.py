import logging

from myapp.extensions import db
from myapp.models import Respuesta, User
from myapp.services.errors import ValidationError
from myapp.services.preguntas import get_pregunta
from myapp.services.validation import clean_text

logger = logging.getLogger(__name__)


def list_respuestas(pregunta_id):
    return get_pregunta(pregunta_id).respuestas


def _find_author(value, errors):
    # bool es subclase de int: se descarta a propósito.
    if isinstance(value, str) and value.isdecimal():
        value = int(value)
    if isinstance(value, int) and not isinstance(value, bool) and 0 < value < 2**31:
        author = db.session.get(User, value)
        if author is not None:
            return author
    errors["autor_id"] = "Elegí un usuario existente"
    return None


def create_respuesta(pregunta_id, data):
    pregunta = get_pregunta(pregunta_id)
    errors = {}
    cuerpo = clean_text(data, "cuerpo", errors)
    autor = _find_author(data.get("autor_id"), errors)
    if errors:
        raise ValidationError(errors)
    respuesta = Respuesta(cuerpo=cuerpo, autor=autor, pregunta=pregunta)
    db.session.add(respuesta)
    db.session.commit()
    logger.info("Respuesta creada id=%s pregunta=%s", respuesta.id, pregunta_id)
    return respuesta
