def clean_text(data, field, errors, max_length=None):
    """Devuelve el texto sin espacios sobrantes y anota el error si no sirve."""
    value = data.get(field)
    if not isinstance(value, str) or not value.strip():
        errors[field] = "Es obligatorio"
        return ""
    value = value.strip()
    if max_length and len(value) > max_length:
        errors[field] = f"Máximo {max_length} caracteres"
    return value
