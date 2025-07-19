import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../file-service')))
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from delete_file.service import delete_file_by_id

import uuid

@pytest.mark.asyncio
async def test_delete_file_by_id_success(monkeypatch):
    session = AsyncMock()
    class DummyFile:
        storage_key = 'key'
        size = 123
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = DummyFile()
    session.execute.return_value = mock_result
    monkeypatch.setattr('delete_file.service.minio_client.remove_object', MagicMock())
    monkeypatch.setattr('delete_file.service.update_user_stat', AsyncMock())
    session.delete = AsyncMock()
    session.commit = AsyncMock()
    result = await delete_file_by_id(str(uuid.uuid4()), 'user_id', session)
    assert result is True

@pytest.mark.asyncio
async def test_delete_file_by_id_not_found():
    session = AsyncMock()
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = None
    session.execute.return_value = mock_result
    result = await delete_file_by_id(str(uuid.uuid4()), 'user_id', session)
    assert result is False
