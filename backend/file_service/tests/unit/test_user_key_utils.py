import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../file-service')))
import pytest
from unittest.mock import AsyncMock, MagicMock
from security.user_key_utils import get_user_encryption_key
from cryptography.fernet import Fernet

@pytest.mark.asyncio
async def test_get_user_encryption_key(monkeypatch):
    master_key = Fernet.generate_key().decode()
    monkeypatch.setenv("USER_KEY_MASTER", master_key)
    user_id = "user_id"
    user_key = Fernet.generate_key()
    encrypted_key = Fernet(master_key.encode()).encrypt(user_key).decode()
    class DummyKeyRow:
        def __init__(self, encrypted_key):
            self.encrypted_key = encrypted_key
    session = AsyncMock()
    session.execute = AsyncMock(return_value=MagicMock(scalar_one_or_none=MagicMock(return_value=DummyKeyRow(encrypted_key))))
    key = await get_user_encryption_key(user_id, session)
    assert key == user_key
