from datetime import date

import pytest

from myapp.domain.agente_ia import AgenteIA
from myapp.domain.autor_factory import AutorFactory
from myapp.domain.categoria import Categoria
from myapp.domain.generador_respuesta import GeneradorRespuesta
from myapp.domain.pregunta import Pregunta


class EstrategiaFalsa(GeneradorRespuesta):
    def generar(self, pregunta):
        return f"Sobre: {pregunta.titulo}"


def nueva_pregunta():
    usuario = AutorFactory.crearAutor("usuario_general", "Ada", "a@x.com", "x")
    return Pregunta("Hola", "Cuerpo", date.today(), usuario, Categoria("General"))


def test_agente_usa_la_estrategia():
    pregunta = nueva_pregunta()

    respuesta = AgenteIA("bot", EstrategiaFalsa()).generarRespuesta(pregunta)

    assert respuesta.cuerpo == "Sobre: Hola"
    assert pregunta.respuestas == [respuesta]


def test_agente_sin_estrategia():
    with pytest.raises(ValueError):
        AgenteIA("bot").generarRespuesta(nueva_pregunta())
