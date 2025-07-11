import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../file-service')))
import pytest
from unittest.mock import AsyncMock, MagicMock
from rename.service import rename_file, rename_folder
from fastapi import HTTPException

@pytest.mark.asyncio
def test_rename_file_success(monkeypatch):
    session = AsyncMock()
    file = MagicMock()
    session.execute.return_value.scalar_one_or_none.return_value = file
    session.commit = AsyncMock()
    session.refresh = AsyncMock()
    result = pytest.run(asyncio=True)(rename_file)('file_id', 'user_id', 'new.txt', session)
    assert result == file

@pytest.mark.asyncio
def test_rename_file_not_found():
    session = AsyncMock()
    session.execute.return_value.scalar_one_or_none.return_value = None
    with pytest.raises(HTTPException) as exc:
        pytest.run(asyncio=True)(rename_file)('file_id', 'user_id', 'new.txt', session)
    assert exc.value.status_code == 404

@pytest.mark.asyncio
def test_rename_folder_success(monkeypatch):
    session = AsyncMock()
    folder = MagicMock()
    session.execute.return_value.scalar_one_or_none.return_value = folder
    session.commit = AsyncMock()
    session.refresh = AsyncMock()
    result = pytest.run(asyncio=True)(rename_folder)('folder_id', 'user_id', 'new_folder', session)
    assert result == folder

@pytest.mark.asyncio
def test_rename_folder_not_found():
    session = AsyncMock()
    session.execute.return_value.scalar_one_or_none.return_value = None
    with pytest.raises(HTTPException) as exc:
        pytest.run(asyncio=True)(rename_folder)('folder_id', 'user_id', 'new_folder', session)
    assert exc.value.status_code == 404
