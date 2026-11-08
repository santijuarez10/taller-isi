from myapp.domain.autor import Autor


class Usuario(Autor):

    def __init__(self, nombre: str, email: str, password: str):
        self.nombre = nombre
        self.email = email
        self.password = password

    def obtenerNombre(self) -> str:
        return self.nombre