class ValidationError(Exception):
    def __init__(self, errors: dict[str, str]):
        super().__init__("Datos inválidos")
        self.errors = errors


class NotFoundError(Exception):
    pass


class ConflictError(Exception):
    pass
