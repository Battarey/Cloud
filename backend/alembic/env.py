import asyncio
from logging.config import fileConfig
from sqlalchemy import pool
from sqlalchemy.ext.asyncio import async_engine_from_config
from alembic import context
import sys
import os

# Добавляем оба каталога моделей в sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../file-service/models')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../user-service/models')))

from file_service.models import FileBase  # noqa
from user_service.models import UserBase  # noqa

config = context.config
fileConfig(config.config_file_name)
# Объединяем метаданные моделей
from sqlalchemy import MetaData
metadata = MetaData()
for base in (FileBase, UserBase):
    for table in base.metadata.tables.values():
        if table.name not in metadata.tables:
            metadata._add_table(table.name, table.schema, table)

target_metadata = metadata

DB_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://clouduser:cloudpass@postgres:5432/cloud_db")
config.set_main_option("sqlalchemy.url", DB_URL)

def run_migrations_offline():
    context.configure(
        url=DB_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()

def do_run_migrations(connection):
    context.configure(
        connection=connection, target_metadata=target_metadata
    )
    with context.begin_transaction():
        context.run_migrations()

async def run_migrations_online():
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section),
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
