"""Alembic environment configuration.

Supports both sync (offline) and async (online) migrations.
Loads database URL from application Settings. Imports model
metadata for autogenerate support.
"""

from __future__ import annotations

import asyncio
from logging.config import fileConfig

from alembic import context
from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config

from arxiv_mcp.config import get_settings

# Import all models so Base.metadata includes them
from arxiv_mcp.db.models import Base  # noqa: F401

# Alembic Config object
config = context.config

# Set up loggers from alembic.ini
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Target metadata for autogenerate
target_metadata = Base.metadata

# Get database URL from application settings
settings = get_settings()

# Convert async URL to sync for Alembic's offline mode
_async_url = settings.database_url
_sync_url = _async_url.replace("+asyncpg", "+psycopg2") if "+asyncpg" in _async_url else _async_url


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    Generates SQL script without connecting to the database.
    """
    context.configure(
        url=_sync_url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    """Run migrations within the given connection."""
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    """Run migrations in async mode using asyncpg."""
    configuration = config.get_section(config.config_ini_section, {})
    configuration["sqlalchemy.url"] = _async_url

    connectable = async_engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode with async engine."""
    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
