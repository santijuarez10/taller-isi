from logging.config import fileConfig

from alembic import context

from myapp import create_app
from myapp.config import Config
from myapp.extensions import db

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name, disable_existing_loggers=False)

target_metadata = db.metadata


class MigrationConfig(Config):
    # Los tests pueden indicar otra base; si no, se usa DATABASE_URL.
    SQLALCHEMY_DATABASE_URI = config.attributes.get(
        "database_url", Config.SQLALCHEMY_DATABASE_URI
    )


app = create_app(MigrationConfig)


def run_migrations_offline() -> None:
    """Run migrations in offline mode."""

    with app.app_context():
        url = db.engine.url.render_as_string(hide_password=False)

        context.configure(
            url=url,
            target_metadata=target_metadata,
            literal_binds=True,
            dialect_opts={"paramstyle": "named"},
        )

        with context.begin_transaction():
            context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in online mode."""

    with app.app_context():
        connectable = db.engine

        with connectable.connect() as connection:
            context.configure(
                connection=connection,
                target_metadata=target_metadata,
            )

            with context.begin_transaction():
                context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
