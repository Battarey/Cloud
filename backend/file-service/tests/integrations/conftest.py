import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
import uuid
import pytest
import pytest_asyncio
import httpx
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy import text
from .minio_utils import ensure_bucket, clear_bucket
from security.jwt import create_access_token
import datetime
from sqlalchemy.orm import sessionmaker
from models.file import File

API_URL = "http://host.docker.internal:8002"

# Глобальная фикстура для подготовки и очистки бакета Minio
@pytest_asyncio.fixture(autouse=True, scope="session")
async def minio_bucket():
    await ensure_bucket()
    yield
    await clear_bucket()

# Очистка всех файлов до и после каждого теста
@pytest_asyncio.fixture(autouse=True, scope="function")
async def clean_db():
    DATABASE_URL = os.environ["DATABASE_URL"]
    engine = create_async_engine(DATABASE_URL, echo=False)
    async with engine.begin() as conn:
        await conn.execute(text("TRUNCATE TABLE files RESTART IDENTITY CASCADE;"))
    yield
    async with engine.begin() as conn:
        await conn.execute(text("TRUNCATE TABLE files RESTART IDENTITY CASCADE;"))

# Асинхронный http-клиент
@pytest_asyncio.fixture(scope="function")
async def async_client():
    async with httpx.AsyncClient(base_url=API_URL, timeout=120.0) as client:
        yield client

# Уникальный user_id для каждого теста
@pytest.fixture
def test_user_id():
    return str(uuid.uuid4())

# Фикстура: только токен, без создания файла
@pytest.fixture
def mock_jwt_empty(test_user_id):
    from datetime import datetime, timedelta, timezone
    exp = datetime.now(timezone.utc) + timedelta(minutes=60)
    payload = {"sub": test_user_id, "exp": exp}
    return create_access_token(payload)

# Фикстура: токен + файл (по умолчанию)
@pytest_asyncio.fixture
async def mock_jwt(test_user_id):
    DATABASE_URL = os.environ["DATABASE_URL"]
    engine = create_async_engine(DATABASE_URL, echo=False)
    async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
    async with async_session() as session:
        test_file = File(
            user_id=test_user_id,
            filename="test.txt",
            size=1,
            content_type="text/plain",
            storage_key="test-key",
            created_at=datetime.datetime.utcnow()
        )
        session.add(test_file)
        await session.commit()
    return create_access_token({"sub": test_user_id})
