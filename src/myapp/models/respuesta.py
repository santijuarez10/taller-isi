from datetime import date

from myapp.extensions import db


class Respuesta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cuerpo = db.Column(db.Text, nullable=False)
    fecha_publicacion = db.Column(db.Date, nullable=False, default=date.today)
    es_aceptada = db.Column(db.Boolean, nullable=False, default=False)
    autor_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    pregunta_id = db.Column(db.Integer, db.ForeignKey("pregunta.id"), nullable=False)

    autor = db.relationship("User", back_populates="respuestas")
    pregunta = db.relationship("Pregunta", back_populates="respuestas")

    def to_dict(self):
        return {
            "id": self.id,
            "cuerpo": self.cuerpo,
            "fecha_publicacion": self.fecha_publicacion.isoformat(),
            "es_aceptada": self.es_aceptada,
            "autor_id": self.autor_id,
            "pregunta_id": self.pregunta_id,
        }
