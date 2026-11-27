"""Persistencia de Pregunta, Categoria y Tag según el diagrama de clases."""

from datetime import date

from myapp.extensions import db

pregunta_tag = db.Table(
    "pregunta_tag",
    db.Column(
        "pregunta_id", db.Integer, db.ForeignKey("pregunta.id"), primary_key=True
    ),
    db.Column("tag_id", db.Integer, db.ForeignKey("tag.id"), primary_key=True),
)


class Categoria(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(80), nullable=False, unique=True)


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(40), nullable=False, unique=True)


class Pregunta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200), nullable=False)
    cuerpo = db.Column(db.Text, nullable=False)
    fecha_publicacion = db.Column(db.Date, nullable=False, default=date.today)
    autor_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    categoria_id = db.Column(db.Integer, db.ForeignKey("categoria.id"), nullable=False)

    autor = db.relationship("User", back_populates="preguntas")
    categoria = db.relationship("Categoria")
    tags = db.relationship("Tag", secondary=pregunta_tag, order_by="Tag.nombre")

    respuestas = db.relationship(
        "Respuesta",
        back_populates="pregunta",
        cascade="all, delete-orphan",
        order_by="Respuesta.id",
    )

    def to_dict(self):
        return {
            "id": self.id,
            "titulo": self.titulo,
            "cuerpo": self.cuerpo,
            "fecha_publicacion": self.fecha_publicacion.isoformat(),
            "autor_id": self.autor_id,
            "categoria": self.categoria.nombre,
            "tags": [tag.nombre for tag in self.tags],
        }
