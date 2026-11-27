from __future__ import annotations

import json
import os
from typing import TYPE_CHECKING
from urllib import error, request

from myapp.domain.generador_respuesta import GeneradorRespuesta

if TYPE_CHECKING:
    from myapp.domain.pregunta import Pregunta


class OpenAIStrategy(GeneradorRespuesta):
    """Genera respuestas usando la API de chat completions de OpenAI.

    Variables de entorno:
        OPENAI_API_KEY (obligatoria), OPENAI_MODEL (opcional).
    """

    URL = "https://api.openai.com/v1/chat/completions"
    MODELO_POR_DEFECTO = "gpt-4o-mini"
    TIMEOUT_SEGUNDOS = 60

    def generar(self, pregunta: Pregunta) -> str:
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError(
                "OpenAIStrategy: falta la variable de entorno OPENAI_API_KEY"
            )

        modelo = os.environ.get("OPENAI_MODEL", self.MODELO_POR_DEFECTO)
        payload = {
            "model": modelo,
            "messages": [
                {"role": "user", "content": f"{pregunta.titulo}\n\n{pregunta.cuerpo}"}
            ],
        }
        req = request.Request(
            self.URL,
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_key}",
            },
            method="POST",
        )

        try:
            with request.urlopen(req, timeout=self.TIMEOUT_SEGUNDOS) as resp:
                data = json.loads(resp.read().decode("utf-8"))
            return data["choices"][0]["message"]["content"]
        except error.HTTPError as e:
            raise RuntimeError(f"OpenAIStrategy: error HTTP {e.code} de la API") from e
        except error.URLError as e:
            raise RuntimeError(
                f"OpenAIStrategy: no se pudo conectar ({e.reason})"
            ) from e
        except (KeyError, IndexError, TypeError, ValueError) as e:
            raise RuntimeError("OpenAIStrategy: respuesta inesperada de la API") from e
