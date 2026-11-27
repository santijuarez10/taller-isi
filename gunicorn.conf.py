"""Configuración de Gunicorn (solo Linux/macOS). Se carga automáticamente."""

import os

bind = f"0.0.0.0:{os.getenv('PORT', '5000')}"
workers = int(os.getenv("WEB_CONCURRENCY", "2"))
accesslog = "-"
