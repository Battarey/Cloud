import pytest
from httpx import AsyncClient
from main import app

@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"

@pytest.fixture
def async_client():
    return AsyncClient(app=app, base_url="http://test")

@pytest.fixture
def mock_jwt():
    return "test.jwt.token"

@pytest.fixture
def mock_minio():
    def _mock(*a, **k): return None
    return _mock

@pytest.fixture
def mock_scan():
    def _mock(result):
        async def inner(*a, **k): return result
        return inner
    return _mock

@pytest.fixture
def mock_stat():
    def _mock(*a, **k): return None
    return _mock
