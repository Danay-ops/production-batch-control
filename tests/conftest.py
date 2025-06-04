import asyncio
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import NullPool, text
from src.production_control.main import app
from httpx import AsyncClient
from src.production_control.db.session import get_db
from src.production_control.db.base import Base
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker


# DATABASE_TEST_URL = "postgresql+asyncpg://user:password@db:5432/testdb_for_test"

from dotenv import load_dotenv
import os

load_dotenv(".env.test")  # Явно указываем файл

DATABASE_TEST_URL = os.getenv("DATABASE_TEST_URL")
if DATABASE_TEST_URL is None:
    raise RuntimeError("DATABASE_TEST_URL is not set")  

# Создаём движок специально для тестов
test_engine = create_async_engine(DATABASE_TEST_URL, poolclass=NullPool)
TestSessionLocal = async_sessionmaker(bind=test_engine, expire_on_commit=False)

# Переопределим зависимость
async def override_get_db():
    async with TestSessionLocal() as session:
        yield session

app.dependency_overrides[get_db] = override_get_db

# Перед запуском тестов создаём таблицы
@pytest.fixture(scope="session", autouse=True)
async def prepare_test_db():
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(autouse=True)
def clean_tables_fixture():
    """Синхронная фикстура, вызывающая асинхронную функцию очистки таблиц."""
    yield  # дожидаемся завершения теста

    async def truncate():
        async with test_engine.begin() as conn:
            tables = await conn.run_sync(lambda sync_conn: list(Base.metadata.tables.keys()))
            for table in tables:
                await conn.execute(text(f"TRUNCATE TABLE {table} RESTART IDENTITY CASCADE"))

    asyncio.run(truncate())
