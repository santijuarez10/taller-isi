from __future__ import annotations

import json
import os
from typing import TYPE_CHECKING
from urllib import error, request

from myapp.domain.generador_respuesta import GeneradorRespuesta

if TYPE_CHECKING:
    from myapp.domain.pregunta import Pregunta


class ModeloLocalStrategy(GeneradorRespuesta):
    """Genera respuestas con un modelo local servido por una API tipo Ollama.

    No requiere API key. Variables de entorno (todas opcionales):
        LOCAL_MODEL_URL (por defecto http://localhost:11434),
        LOCAL_MODEL_NAME (por defecto llama3).
    """

    URL_POR_DEFECTO = "http://localhost:11434"
    MODELO_POR_DEFECTO = "llama3"
    TIMEOUT_SEGUNDOS = 120

    def generar(self, pregunta: Pregunta) -> str:
        base_url = os.environ.get("LOCAL_MODEL_URL", self.URL_POR_DEFECTO).rstrip("/")
        modelo = os.environ.get("LOCAL_MODEL_NAME", self.MODELO_POR_DEFECTO)
        payload = {
            "model": modelo,
            "prompt": f"{pregunta.titulo}\n\n{pregunta.cuerpo}",
            "stream": False,
        }
        req = request.Request(
            f"{base_url}/api/generate",
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )

        try:
            with request.urlopen(req, timeout=self.TIMEOUT_SEGUNDOS) as resp:
                data = json.loads(resp.read().decode("utf-8"))
            return data["response"]
        except error.HTTPError as e:
            raise RuntimeError(
                f"ModeloLocalStrategy: error HTTP {e.code} del servidor local"
            ) from e
        except error.URLError as e:
            raise RuntimeError(
                f"ModeloLocalStrategy: no se pudo conectar a {base_url} ({e.reason})"
            ) from e
        except (KeyError, TypeError, ValueError) as e:
            raise RuntimeError(
                "ModeloLocalStrategy: respuesta inesperada del servidor local"
            ) from e
