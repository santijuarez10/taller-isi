from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from myapp.domain.pregunta import Pregunta


class GeneradorRespuesta(ABC):
    """Interfaz Strategy: genera el texto de una respuesta a una pregunta."""

    @abstractmethod
    def generar(self, pregunta: Pregunta) -> str:
        pass
