import pytest
from statistics.service import update_user_stat
from models.user import User
from models.stat_update import StatUpdate
from unittest.mock import AsyncMock
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
import uuid

@pytest.mark.asyncio
async def test_update_user_stat_upload(monkeypatch):
    session = AsyncMock(spec=AsyncSession)
    user = User(id=uuid.uuid4(), email="test@example.com", username="testuser", hashed_password="hashed", files_count=0, files_size=0, free_space=1000)
    from unittest.mock import MagicMock
    execute_mock = MagicMock()
    execute_mock.scalar_one_or_none.return_value = user
    session.execute.return_value = execute_mock
    session.commit = AsyncMock()
    session.refresh = AsyncMock()
    data = StatUpdate(user_id=user.id, action="upload", file_size=100)
    result = await update_user_stat(data, session)
    assert result["status"] == "ok"
    assert user.files_count == 1
    assert user.files_size == 100
    assert user.free_space == 900

@pytest.mark.asyncio
async def test_update_user_stat_delete(monkeypatch):
    session = AsyncMock(spec=AsyncSession)
    user = User(id=uuid.uuid4(), email="test@example.com", username="testuser", hashed_password="hashed", files_count=2, files_size=200, free_space=800)
    from unittest.mock import MagicMock
    execute_mock = MagicMock()
    execute_mock.scalar_one_or_none.return_value = user
    session.execute.return_value = execute_mock
    session.commit = AsyncMock()
    session.refresh = AsyncMock()
    data = StatUpdate(user_id=user.id, action="delete", file_size=100)
    result = await update_user_stat(data, session)
    assert result["status"] == "ok"
    assert user.files_count == 1
    assert user.files_size == 100
    assert user.free_space == 900

@pytest.mark.asyncio
async def test_update_user_stat_user_not_found():
    session = AsyncMock(spec=AsyncSession)
    from unittest.mock import MagicMock
    execute_mock = MagicMock()
    execute_mock.scalar_one_or_none.return_value = None
    session.execute.return_value = execute_mock
    data = StatUpdate(user_id=uuid.uuid4(), action="upload", file_size=100)
    with pytest.raises(HTTPException) as exc:
        await update_user_stat(data, session)
    assert exc.value.status_code == 404

@pytest.mark.asyncio
async def test_update_user_stat_invalid_action():
    session = AsyncMock(spec=AsyncSession)
    user = User(id=uuid.uuid4(), email="test@example.com", username="testuser", hashed_password="hashed", files_count=0, files_size=0, free_space=1000)
    session.execute.return_value.scalar_one_or_none.return_value = user
    data = StatUpdate(user_id=user.id, action="invalid", file_size=100)
    with pytest.raises(HTTPException) as exc:
        await update_user_stat(data, session)
    assert exc.value.status_code == 400
