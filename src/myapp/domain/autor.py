from abc import ABC, abstractmethod


class Autor(ABC):

    @abstractmethod
    def obtenerNombre(self) -> str:
        pass