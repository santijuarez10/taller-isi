from flask import request

from myapp.services.errors import ValidationError


def json_object():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        raise ValidationError({"body": "Se esperaba un objeto JSON"})
    return data
