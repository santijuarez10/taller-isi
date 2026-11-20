    
from __future__ import annotations

from datetime import date
from typing import TYPE_CHECKING

from myapp.domain.votable import Votable
from myapp.domain.categoria import Categoria
from myapp.domain.tag import Tag

if TYPE_CHECKING:
    from myapp.domain.usuario import Usuario


class Pregunta(Votable):

    def __init__(
        self,
        titulo: str,
        cuerpo: str,
        fechaPublicacion: date,
        usuario: Usuario,
        categoria: Categoria,
        tags: list[Tag] | None = None
    ):
        # atributos propios
        self.titulo = titulo
        self.cuerpo = cuerpo
        self.fechaPublicacion = fechaPublicacion

        # relaciones con otras clases
        self.usuario = usuario
        self.categoria = categoria
        self.tags = list(tags) if tags is not None else []
        
        # una pregunta puede tener muchas respuestas
        self.respuestas = []
