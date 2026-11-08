from myapp.domain.usuario import Usuario
from myapp.domain.votable import Votable


class Voto:

    def __init__(self, valor: int, usuario: Usuario, votable: Votable):
        self.valor = valor
        self.usuario = usuario
        self.votable = votable