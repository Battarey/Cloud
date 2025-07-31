import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../file-service')))
import pytest
from unittest.mock import AsyncMock, MagicMock
from upload_file.service import save_uploaded_file
from cryptography.fernet import Fernet
import uuid
import datetime
import sys

@pytest.mark.asyncio
async def test_file_encryption_on_upload(monkeypatch):
    master_key = Fernet.generate_key().decode()
    monkeypatch.setenv("USER_KEY_MASTER", master_key)
    user_id = str(uuid.uuid4())
    user_key = Fernet.generate_key()
    encrypted_key = Fernet(master_key.encode()).encrypt(user_key).decode()
    session = AsyncMock()
    file_id = str(uuid.uuid4())
    class DummyKeyRow:
        def __init__(self, encrypted_key):
            self.encrypted_key = encrypted_key
    # Оставляем оригинальный FileModel, side_effect возвращает MagicMock с нужными атрибутами
    session.execute = AsyncMock(side_effect=[
        MagicMock(scalar_one_or_none=MagicMock(return_value=None)),  # нет дубликата
        MagicMock(scalar_one_or_none=MagicMock(return_value=DummyKeyRow(encrypted_key)))  # ключ пользователя
    ])
    upload = MagicMock()
    upload.filename = "test.txt"
    upload.content_type = "text/plain"
    upload.read = AsyncMock(return_value=b"hello world")
    upload.seek = AsyncMock()
    put_object_func = AsyncMock()
    # Мокаем session.add, чтобы присваивать created_at
    orig_add = session.add
    def add_with_created_at(obj):
        if not hasattr(obj, "created_at") or obj.created_at is None:
            obj.created_at = datetime.datetime.now(datetime.timezone.utc)
        if orig_add:
            orig_add(obj)
    session.add = add_with_created_at
    result = await save_uploaded_file(upload, user_id, session, put_object_func=put_object_func)
    args, kwargs = put_object_func.call_args
    encrypted_data = kwargs['data'].getvalue()
    assert encrypted_data != b"hello world"
    decrypted = Fernet(user_key).decrypt(encrypted_data)
    assert decrypted == b"hello world"
