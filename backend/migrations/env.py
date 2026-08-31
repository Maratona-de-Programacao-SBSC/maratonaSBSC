import os
from logging.config import fileConfig
from urllib.parse import quote_plus

from alembic import context
from sqlalchemy import create_engine, pool


config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)


def _database_url() -> str:
    usuario = quote_plus(os.environ["DATABASE_USER"])
    senha = quote_plus(os.environ["DATABASE_PASSWORD"])
    host = os.getenv("DATABASE_HOST", "localhost")
    porta = os.getenv("DATABASE_PORT", "3306")
    banco = quote_plus(os.environ["DATABASE"])
    return f"mysql+mysqlconnector://{usuario}:{senha}@{host}:{porta}/{banco}"


def run_migrations_offline() -> None:
    context.configure(
        url=_database_url(),
        target_metadata=None,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    engine = create_engine(_database_url(), poolclass=pool.NullPool)
    with engine.connect() as connection:
        context.configure(connection=connection, target_metadata=None)
        with context.begin_transaction():
            context.run_migrations()
    engine.dispose()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
