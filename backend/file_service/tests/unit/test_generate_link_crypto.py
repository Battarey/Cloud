import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../file-service')))
import pytest
from unittest.mock import AsyncMock, MagicMock
from generate_link.router import direct_download_file
from cryptography.fernet import Fernet
import uuid
import download_file.service

@pytest.mark.asyncio
async def test_direct_download_file_crypto(monkeypatch):
    master_key = Fernet.generate_key().decode()
    monkeypatch.setenv("USER_KEY_MASTER", master_key)
    user_id = "user_id"
    user_key = Fernet.generate_key()
    encrypted_key = Fernet(master_key.encode()).encrypt(user_key).decode()
    session = AsyncMock()
    file_id = str(uuid.uuid4())
    class DummyKeyRow:
        def __init__(self, encrypted_key):
            self.encrypted_key = encrypted_key
    class DummyFile:
        def __init__(self, user_id, file_id):
            self.id = uuid.UUID(file_id)
            self.user_id = user_id
            self.filename = "test.txt"
            self.content_type = "text/plain"
            self.storage_key = "key"
    class DummyResponse:
        async def read(self):
            return Fernet(user_key).encrypt(b"hello world")
    session.execute = AsyncMock(side_effect=[
        MagicMock(scalar_one_or_none=MagicMock(return_value=DummyFile(user_id, file_id))),
        MagicMock(scalar_one_or_none=MagicMock(return_value=DummyKeyRow(encrypted_key)))
    ])
    # Мокаем функцию async_get_object, чтобы не обращаться к MinIO
    async def mock_get_object(bucket, key):
        return DummyResponse()
    # Проверяем endpoint, явно передавая мок
    response = await direct_download_file(file_id, user_id, session, get_object_func=mock_get_object)
    assert response.body == b"hello world"
