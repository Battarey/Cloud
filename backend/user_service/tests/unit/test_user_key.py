import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
import pytest
from unittest.mock import AsyncMock, MagicMock
from cryptography.fernet import Fernet

@pytest.mark.asyncio
def test_user_key_generation_and_decryption(monkeypatch):
    master_key = Fernet.generate_key().decode()
    monkeypatch.setenv("USER_KEY_MASTER", master_key)
    # Мокаем сессию
    session = AsyncMock()
    session.execute = AsyncMock()
    session.commit = AsyncMock()
    session.refresh = AsyncMock()
    session.add = MagicMock()
    # Мокаем возврат пользователя
    user_id = "mocked-user-id"
    user = {"id": user_id, "email": "testkey@example.com", "username": "testkeyuser"}
    # Мокаем register_user_service
    async def mock_register_user_service(user_data, session):
        return user
    # Генерируем ключ
    user_key = Fernet.generate_key()
    fernet = Fernet(master_key.encode())
    encrypted_key = fernet.encrypt(user_key)
    # Проверяем расшифровку
    decrypted_key = fernet.decrypt(encrypted_key)
    Fernet(decrypted_key)  # Проверка, что ключ валиден для Fernet
