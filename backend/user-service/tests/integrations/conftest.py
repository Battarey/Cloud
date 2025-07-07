import pytest
import pytest_asyncio
import asyncio
import httpx
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
import os

# URL для тестового API
API_URL = os.getenv("API_URL", "http://host.docker.internal:8000")

@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()

@pytest_asyncio.fixture(scope="function")
async def async_client():
    async with httpx.AsyncClient(base_url=API_URL, timeout=10.0) as client:
        yield client

# TODO: добавить фикстуры для очистки БД и Redis между тестами
