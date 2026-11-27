from myapp.domain.admin import Admin
from myapp.domain.autor_factory import AutorFactory
from myapp.domain.usuario_general import UsuarioGeneral


def test_crear_admin():
    autor = AutorFactory.crearAutor("admin", "Santiago", "santi@gmail.com", "1234")

    assert isinstance(autor, Admin)
    assert autor.obtenerNombre() == "Santiago"


def test_crear_usuario_general():
    autor = AutorFactory.crearAutor("usuario_general", "Juan", "juan@gmail.com", "1234")

    assert isinstance(autor, UsuarioGeneral)
    assert autor.obtenerNombre() == "Juan"
