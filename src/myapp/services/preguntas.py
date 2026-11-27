import logging

from myapp.extensions import db
from myapp.models import Categoria, Pregunta, Tag, User
from myapp.services.errors import NotFoundError, ValidationError
from myapp.services.validation import clean_text

logger = logging.getLogger(__name__)

FIELDS = ("titulo", "cuerpo", "autor_id", "categoria", "tags")


def list_preguntas():
    query = db.select(Pregunta).order_by(
        Pregunta.fecha_publicacion.desc(), Pregunta.id.desc()
    )
    return db.session.scalars(query).all()


def get_pregunta(pregunta_id):
    pregunta = db.session.get(Pregunta, pregunta_id)
    if pregunta is None:
        raise NotFoundError("Pregunta no encontrada")
    return pregunta


def _parse_tags(value, errors):
    """Acepta una lista (API) o un texto separado por comas (formulario)."""
    if value is None:
        return []
    if isinstance(value, str):
        value = value.split(",")
    if not isinstance(value, list) or not all(isinstance(t, str) for t in value):
        errors["tags"] = "Debe ser una lista de textos"
        return []
    names = list(dict.fromkeys(t.strip().lower() for t in value if t.strip()))
    if any(len(name) > 40 for name in names):
        errors["tags"] = "Cada tag admite hasta 40 caracteres"
    return names


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


def _validate(data):
    errors = {}
    titulo = clean_text(data, "titulo", errors, 200)
    cuerpo = clean_text(data, "cuerpo", errors)
    categoria = clean_text(data, "categoria", errors, 80)
    tags = _parse_tags(data.get("tags"), errors)
    autor = _find_author(data.get("autor_id"), errors)
    if errors:
        raise ValidationError(errors)
    return titulo, cuerpo, autor, categoria, tags


def _get_or_create(model, nombre):
    instance = db.session.scalar(db.select(model).where(model.nombre == nombre))
    if instance is None:
        instance = model(nombre=nombre)
        db.session.add(instance)
    return instance


def _apply(pregunta, values):
    titulo, cuerpo, autor, categoria, tags = values
    # Se buscan antes de asignar para no disparar un guardado a medias.
    categoria_model = _get_or_create(Categoria, categoria)
    tag_models = [_get_or_create(Tag, name) for name in tags]
    pregunta.titulo = titulo
    pregunta.cuerpo = cuerpo
    pregunta.autor = autor
    pregunta.categoria = categoria_model
    pregunta.tags = tag_models


def create_pregunta(data):
    values = _validate(data)
    pregunta = Pregunta()
    with db.session.no_autoflush:
        _apply(pregunta, values)
        db.session.add(pregunta)
    db.session.commit()
    logger.info("Pregunta creada id=%s", pregunta.id)
    return pregunta


def update_pregunta(pregunta_id, data):
    """Actualiza los campos presentes en data; el resto queda igual."""
    pregunta = get_pregunta(pregunta_id)
    current = pregunta.to_dict()
    merged = {field: current[field] for field in FIELDS}
    merged |= {field: data[field] for field in FIELDS if field in data}
    values = _validate(merged)
    with db.session.no_autoflush:
        _apply(pregunta, values)
    db.session.commit()
    logger.info("Pregunta actualizada id=%s", pregunta.id)
    return pregunta


def delete_pregunta(pregunta_id):
    db.session.delete(get_pregunta(pregunta_id))
    db.session.commit()
    logger.info("Pregunta borrada id=%s", pregunta_id)
