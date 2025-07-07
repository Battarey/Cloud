
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

import pytest
from statistics.service import update_user_stat
from models.user import User
from unittest.mock import AsyncMock
from sqlalchemy.ext.asyncio import AsyncSession

@pytest.mark.asyncio
async def test_update_user_stat_upload(monkeypatch):
    session = AsyncMock(spec=AsyncSession)
    import uuid
    user = User(id=uuid.uuid4(), email="test@example.com", username="testuser", hashed_password="hashed", files_count=0, files_size=0, free_space=1000)
    from unittest.mock import MagicMock
    execute_mock = MagicMock()
    execute_mock.scalar_one_or_none.return_value = user
    session.execute.return_value = execute_mock
    session.commit = AsyncMock()
    session.refresh = AsyncMock()
    from models.stat_update import StatUpdate
    data = StatUpdate(user_id=user.id, action="upload", file_size=100)
    result = await update_user_stat(data, session)
    assert result["status"] == "ok"
    assert user.files_count == 1
    assert user.files_size == 100
    assert user.free_space == 900
