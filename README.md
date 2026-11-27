# taller-isi — Plataforma de Preguntas y Respuestas

Aplicación web y API JSON hechas con Flask a partir del diagrama de clases UML
(`diagrama-jpeg.jpeg`, justificación en `justificacion.txt`).

Integrantes:
    Santiago Juarez,
    Justo Campoy,
    Enzo Mercado,
    Santiago Miloch

## Requisitos

[uv](https://docs.astral.sh/uv/). uv instala Python 3.14 y las dependencias.

## Puesta en marcha

```bash
git clone <repository>
cd <carpeta-del-proyecto>
uv sync
uv run alembic upgrade head
uv run flask --app myapp run --debug
```

Abrir http://localhost:5000 (primero crear un usuario y después una pregunta).

La configuración es opcional en desarrollo. Para cambiarla, copiar
`.env.example` a `.env` y editarlo. El `.env` no se sube a Git.

| Variable | Para qué | Por defecto |
|---|---|---|
| `APP_ENV` | `development` o `production` | `development` |
| `SECRET_KEY` | Firma de la sesión; obligatoria en producción | clave de desarrollo |
| `DATABASE_URL` | Base de datos | `sqlite:///app.db` (en `instance/`) |
| `LOG_LEVEL` | Nivel de logging (a stdout) | `INFO` |
| `PORT` | Puerto de Gunicorn | `5000` |

Para otro puerto en desarrollo: `uv run flask --app myapp run --port 8080`.

## Tests y calidad

```bash
uv run pytest
uv run ruff check .
uv run ruff format .
```

GitHub Actions (`.github/workflows/ci.yml`) corre lint y tests en cada push y PR.

## Migraciones

```bash
uv run alembic upgrade head                           # aplicar
uv run alembic revision --autogenerate -m "mensaje"   # crear (y revisar)
uv run alembic downgrade -1                           # volver atrás
```

## Rutas web

| Método y ruta | Acción |
|---|---|
| `GET /users`, `GET /preguntas` | Listar |
| `GET /users/<id>`, `GET /preguntas/<id>` | Ver |
| `GET .../new`, `POST /users`, `POST /preguntas` | Crear |
| `GET .../<id>/edit`, `POST .../<id>` | Editar |
| `POST .../<id>/delete` | Borrar |

## API JSON

| Método y ruta | Respuesta correcta |
|---|---|
| `GET /health` | 200 `{"status": "ok"}` |
| `GET /api/users`, `GET /api/preguntas` | 200 |
| `GET /api/users/<id>`, `GET /api/preguntas/<id>` | 200 |
| `POST /api/users`, `POST /api/preguntas` | 201 |
| `PATCH /api/users/<id>`, `PATCH /api/preguntas/<id>` | 200 |
| `DELETE /api/users/<id>`, `DELETE /api/preguntas/<id>` | 204 |

Errores: 400 datos inválidos, 404 no existe, 409 email repetido o usuario con
preguntas.

Cuerpos de ejemplo:

```json
{"name": "Ada Lovelace", "email": "ada@example.com"}
```

```json
{"titulo": "¿Qué es un Blueprint?", "cuerpo": "...", "autor_id": 1,
 "categoria": "Flask", "tags": ["python", "web"]}
```

## Producción

```bash
uv run alembic upgrade head
uv run gunicorn "myapp:create_app()"
```

Definir `APP_ENV=production`, `SECRET_KEY` y, para PostgreSQL,
`DATABASE_URL=postgresql+psycopg://usuario:clave@host:5432/base`.
Gunicorn no funciona en Windows nativo: usar Linux, macOS o WSL.

## Estructura

| Carpeta en `src/myapp/` | Contenido |
|---|---|
| `web/`, `templates/`, `static/` | Páginas HTML (Jinja2) |
| `api/` | API JSON y `/health` |
| `services/` | Validación y reglas, compartidas por web y API |
| `models/` | Tablas (SQLAlchemy) |
| `domain/` | Clases del diagrama UML (patrones Strategy y Factory) |

## Alcance actual

La web y la API manejan usuarios y preguntas (con categoría y tags).
Respuestas, votos y el agente de IA están implementados en `domain/`, pero
todavía no tienen base de datos ni pantallas. No hay autenticación ni protección
CSRF: están previstas para iteraciones posteriores.
