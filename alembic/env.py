import asyncio
from logging.config import fileConfig
import os
import sys
from sqlalchemy.ext.asyncio import async_engine_from_config
from alembic import context

# добавляем путь к src
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from production_control.db.models import shift_tasks
from src.production_control.db.base import Base
from production_control.db.models import product  # <-- подтяни ВСЕ модели, чтобы Alembic их видел

# this is the Alembic Config object
config = context.config

# Interpret the config file for Python logging
fileConfig(config.config_file_name)

# Создаём metadata
target_metadata = Base.metadata

#postgresql+asyncpg://user:password@db/testdb

# Указываем URL (можно из переменной окружения)
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+asyncpg://user:password@db:5432/testdb"
)

def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    context.configure(
        url=DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online():
    """Run migrations in 'online' mode."""

    connectable = async_engine_from_config(
        {
            "sqlalchemy.url": DATABASE_URL,
        },
        prefix="sqlalchemy.",
        poolclass=None,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def do_run_migrations(connection):
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        compare_type=True  # важно для изменения типов
    )

    with context.begin_transaction():
        context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())
