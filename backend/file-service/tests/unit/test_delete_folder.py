import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../file-service')))
import pytest
from unittest.mock import AsyncMock, MagicMock
from delete_folder.service import delete_folder_by_id

@pytest.mark.asyncio
def test_delete_folder_by_id_success(monkeypatch):
    session = AsyncMock()
    folder = MagicMock()
    session.execute.return_value.scalar_one_or_none.return_value = folder
    session.delete = AsyncMock()
    session.commit = AsyncMock()
    result = pytest.run(asyncio=True)(delete_folder_by_id)('folder_id', 'user_id', session)
    assert result is True

@pytest.mark.asyncio
def test_delete_folder_by_id_not_found():
    session = AsyncMock()
    session.execute.return_value.scalar_one_or_none.return_value = None
    result = pytest.run(asyncio=True)(delete_folder_by_id)('folder_id', 'user_id', session)
    assert result is False
