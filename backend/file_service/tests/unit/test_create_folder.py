import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../file-service')))
import pytest
from unittest.mock import AsyncMock, MagicMock
from create_folder.service import create_folder

@pytest.mark.asyncio
async def test_create_folder(monkeypatch):
    session = AsyncMock()
    session.add = AsyncMock()
    session.commit = AsyncMock()
    session.refresh = AsyncMock()
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = None
    session.execute.return_value = mock_result
    folder = await create_folder('user_id', 'folder_name', session)
    assert folder is not None
    assert hasattr(folder, 'filename')
