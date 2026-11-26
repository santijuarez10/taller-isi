from __future__ import annotations

from datetime import date
from typing import TYPE_CHECKING

from myapp.domain.autor import Autor
from myapp.domain.generador_respuesta import GeneradorRespuesta
from myapp.domain.respuesta import Respuesta

if TYPE_CHECKING:
    from myapp.domain.pregunta import Pregunta


class AgenteIA(Autor):
    """Autor artificial que delega la generacion de texto en una estrategia.

    La estrategia se inyecta desde afuera (constructor o setter) y puede
    cambiarse en tiempo de ejecucion. AgenteIA nunca la instancia por si mismo.
    """

    def __init__(self, nombre: str, estrategia: GeneradorRespuesta | None = None):
        self.nombre = nombre
        self._estrategia: GeneradorRespuesta | None = None
        self.estrategia = estrategia

    @property
    def estrategia(self) -> GeneradorRespuesta | None:
        return self._estrategia

    @estrategia.setter
    def estrategia(self, estrategia: GeneradorRespuesta | None) -> None:
        if estrategia is not None and not isinstance(estrategia, GeneradorRespuesta):
            raise TypeError(
                "La estrategia debe implementar GeneradorRespuesta, "
                f"se recibio {type(estrategia).__name__}"
            )
        self._estrategia = estrategia

    def obtenerNombre(self) -> str:
        return self.nombre

    def generarRespuesta(self, pregunta: Pregunta) -> Respuesta:
        if self._estrategia is None:
            raise ValueError(
                f"AgenteIA '{self.nombre}' no tiene una estrategia configurada: "
                "asignale un GeneradorRespuesta antes de generar respuestas"
            )

        texto = self._estrategia.generar(pregunta)
        return Respuesta(texto, date.today(), False, self, pregunta)