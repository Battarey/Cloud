import pytest
import pytest_asyncio
import asyncio
import httpx
from sqlalchemy.ext.asyncio import create_async_engine
import os
from sqlalchemy import text

# URL для тестового API file-service
API_URL = "http://host.docker.internal:8002"

@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()

@pytest_asyncio.fixture(autouse=True, scope="function")
async def clean_db():
    # Очистка всех таблиц перед каждым тестом
    DATABASE_URL = os.environ["DATABASE_URL"]
    engine = create_async_engine(DATABASE_URL, echo=False)
    async with engine.begin() as conn:
        await conn.execute(text("TRUNCATE TABLE files RESTART IDENTITY CASCADE;"))
    yield

@pytest_asyncio.fixture(scope="function")
async def async_client():
    async with httpx.AsyncClient(base_url=API_URL, timeout=10.0) as client:
        yield client
