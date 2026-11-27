from __future__ import annotations

import json
import os
from typing import TYPE_CHECKING
from urllib import error, request

from myapp.domain.generador_respuesta import GeneradorRespuesta

if TYPE_CHECKING:
    from myapp.domain.pregunta import Pregunta


class GeminiStrategy(GeneradorRespuesta):
    """Genera respuestas usando la API generateContent de Google Gemini.

    Variables de entorno:
        GEMINI_API_KEY (obligatoria), GEMINI_MODEL (opcional).
    """

    URL_BASE = "https://generativelanguage.googleapis.com/v1beta/models"
    MODELO_POR_DEFECTO = "gemini-2.5-flash"
    TIMEOUT_SEGUNDOS = 60

    def generar(self, pregunta: Pregunta) -> str:
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            raise RuntimeError(
                "GeminiStrategy: falta la variable de entorno GEMINI_API_KEY"
            )

        modelo = os.environ.get("GEMINI_MODEL", self.MODELO_POR_DEFECTO)
        payload = {
            "contents": [
                {"parts": [{"text": f"{pregunta.titulo}\n\n{pregunta.cuerpo}"}]}
            ]
        }
        req = request.Request(
            f"{self.URL_BASE}/{modelo}:generateContent",
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Content-Type": "application/json",
                "x-goog-api-key": api_key,
            },
            method="POST",
        )

        try:
            with request.urlopen(req, timeout=self.TIMEOUT_SEGUNDOS) as resp:
                data = json.loads(resp.read().decode("utf-8"))
            return data["candidates"][0]["content"]["parts"][0]["text"]
        except error.HTTPError as e:
            raise RuntimeError(f"GeminiStrategy: error HTTP {e.code} de la API") from e
        except error.URLError as e:
            raise RuntimeError(
                f"GeminiStrategy: no se pudo conectar ({e.reason})"
            ) from e
        except (KeyError, IndexError, TypeError, ValueError) as e:
            raise RuntimeError("GeminiStrategy: respuesta inesperada de la API") from e
