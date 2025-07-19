import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../file-service')))
import pytest
from unittest.mock import AsyncMock, MagicMock
from delete_folder.service import delete_folder_by_id

@pytest.mark.asyncio
async def test_delete_folder_by_id_success(monkeypatch):
    session = AsyncMock()
    class DummyFolder:
        storage_key = 'prefix/'
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = DummyFolder()
    session.execute.return_value = mock_result
    session.delete = AsyncMock()
    session.commit = AsyncMock()
    import uuid
    result = await delete_folder_by_id(str(uuid.uuid4()), 'user_id', session)
    assert result is True

@pytest.mark.asyncio
async def test_delete_folder_by_id_not_found():
    session = AsyncMock()
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = None
    session.execute.return_value = mock_result
    import uuid
    result = await delete_folder_by_id(str(uuid.uuid4()), 'user_id', session)
    assert result is False
