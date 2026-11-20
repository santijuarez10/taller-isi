      
from __future__ import annotations

from datetime import date
from typing import TYPE_CHECKING

from myapp.domain.votable import Votable

if TYPE_CHECKING:
    from myapp.domain.autor import Autor
    from myapp.domain.pregunta import Pregunta


class Respuesta(Votable):

    def __init__(
        self,
        cuerpo: str,
        fechaPublicacion: date,
        esAceptada: bool,
        autor: Autor,
        pregunta: Pregunta
    ):
        
        # atributos propios
        self.cuerpo = cuerpo
        self.fechaPublicacion = fechaPublicacion
        self.esAceptada = esAceptada

        # relaciones con otras clases
        self.autor = autor
        self.pregunta = pregunta

        # registramos la respuesta en su pregunta
        pregunta.respuestas.append(self)
        
        
