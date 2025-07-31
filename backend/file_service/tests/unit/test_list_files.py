import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../file-service')))
import pytest
from unittest.mock import AsyncMock, MagicMock
from list_files.service import list_user_files

@pytest.mark.asyncio
async def test_list_user_files(monkeypatch):
    session = AsyncMock()
    mock_result = MagicMock()
    mock_scalars = MagicMock()
    mock_scalars.all.return_value = ['file1', 'file2']
    mock_result.scalars.return_value = mock_scalars
    session.execute.return_value = mock_result
    files = await list_user_files('user_id', None, session)
    assert files == ['file1', 'file2']

@pytest.mark.asyncio
async def test_list_user_files_with_folder(monkeypatch):
    session = AsyncMock()
    mock_result = MagicMock()
    mock_scalars = MagicMock()
    mock_scalars.all.return_value = ['file1']
    mock_result.scalars.return_value = mock_scalars
    session.execute.return_value = mock_result
    files = await list_user_files('user_id', 'folder_id', session)
    assert files == ['file1']
