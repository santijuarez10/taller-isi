from myapp.domain.votable import Votable


class Pregunta(Votable):

    def __init__(self, titulo: str, cuerpo: str, fechaPublicacion: str):
        self.titulo = titulo
        self.cuerpo = cuerpo
        self.fechaPublicacion = fechaPublicacion