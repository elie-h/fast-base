import asyncio

import structlog
from asyncpg import Connection
from sqlalchemy import pool
from sqlalchemy.ext.asyncio import async_engine_from_config
from sqlmodel import SQLModel

from alembic import context
from app.core.config import config as app_config
from app.core.logging import setup_logging
from app.db.models import Song  # noqa

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

setup_logging(json_logs=app_config.JSON_LOGGING, log_level=app_config.LOG_LEVEL)
logger = structlog.stdlib.get_logger("alembic.migration")


# add your model's MetaData object here
target_metadata = SQLModel.metadata


def get_url():
    return app_config.DATABASE_URL


def run_migrations_offline():
    """Run migrations in 'offline' mode.
    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.
    Calls to context.execute() here emit the given string to the
    script output.
    """
    # url = config.get_main_option("sqlalchemy.url")
    url = get_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    if connection is None:
        raise Exception("No connection")
    context.configure(connection=connection, target_metadata=target_metadata)  # type: ignore

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online():
    """Run migrations in 'online' mode.
    In this scenario we need to create an Engine
    and associate a connection with the context.
    """
    configuration = config.get_section(config.config_ini_section)
    assert isinstance(configuration, dict)
    configuration["sqlalchemy.url"] = get_url()
    connectable = async_engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())
