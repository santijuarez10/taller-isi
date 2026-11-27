from myapp.extensions import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)

    preguntas = db.relationship("Pregunta", back_populates="autor")
    respuestas = db.relationship("Respuesta", back_populates="autor")

    def to_dict(self):
        return {"id": self.id, "name": self.name, "email": self.email}

    def __repr__(self):
        return f"<User {self.email}>"
