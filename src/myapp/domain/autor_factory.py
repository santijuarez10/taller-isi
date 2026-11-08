from myapp.domain.admin import Admin
from myapp.domain.autor import Autor
from myapp.domain.usuario_general import UsuarioGeneral


class AutorFactory:

    @staticmethod
    def crearAutor(tipo: str, nombre: str, email: str, password: str) -> Autor:
        if tipo == "admin":
            return Admin(nombre, email, password)

        elif tipo == "usuario_general":
            return UsuarioGeneral(nombre, email, password)

        else:
            raise ValueError(f"Tipo de autor no válido: {tipo}")