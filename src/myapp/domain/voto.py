from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from myapp.domain.usuario import Usuario
    from myapp.domain.votable import Votable


class Voto:
    def __init__(self, valor: int, usuario: Usuario, votable: Votable):
        # atributo propio
        self.valor = valor

        # relaciones con otras clases
        self.usuario = usuario
        self.votable = votable
