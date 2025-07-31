import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../file-service')))
import pytest
from unittest.mock import AsyncMock, MagicMock
from download_file.service import get_file_for_download
from cryptography.fernet import Fernet
import uuid

@pytest.mark.asyncio
async def test_file_decryption_on_download(monkeypatch):
    master_key = Fernet.generate_key().decode()
    monkeypatch.setenv("USER_KEY_MASTER", master_key)
    user_id = "user_id"
    user_key = Fernet.generate_key()
    encrypted_key = Fernet(master_key.encode()).encrypt(user_key).decode()
    # Мокаем session
    session = AsyncMock()
    file_id = str(uuid.uuid4())
    class DummyKeyRow:
        def __init__(self, encrypted_key):
            self.encrypted_key = encrypted_key
    class DummyResponse:
        async def read(self):
            return Fernet(user_key).encrypt(b"hello world")
    class DummyFile:
        def __init__(self, user_id, file_id):
            self.id = uuid.UUID(file_id)
            self.user_id = user_id
            self.filename = "test.txt"
            self.content_type = "text/plain"
            self.storage_key = "key"
    # Мокаем select: сначала файл, потом ключ
    session.execute = AsyncMock(side_effect=[
        MagicMock(scalar_one_or_none=MagicMock(return_value=DummyFile(user_id, file_id))),
        MagicMock(scalar_one_or_none=MagicMock(return_value=DummyKeyRow(encrypted_key)))
    ])
    # Мокаем get_object_func
    async def dummy_get_object_func(*args, **kwargs):
        return DummyResponse()
    # Проверяем расшифровку
    data, file = await get_file_for_download(file_id, user_id, session, get_object_func=dummy_get_object_func)
    assert data == b"hello world"
