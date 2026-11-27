from pathlib import Path

from alembic import command
from alembic.config import Config

ROOT = Path(__file__).resolve().parents[1]


def test_migrations_match_models(tmp_path):
    config = Config(ROOT / "alembic.ini")
    config.attributes["database_url"] = f"sqlite:///{tmp_path / 'test.db'}"

    command.upgrade(config, "head")
    command.check(config)  # falla si los modelos y las migraciones difieren
    command.downgrade(config, "base")
