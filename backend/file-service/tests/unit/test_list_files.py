import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../file-service')))
import pytest
from unittest.mock import AsyncMock
from list_files.service import list_user_files

@pytest.mark.asyncio
def test_list_user_files(monkeypatch):
    session = AsyncMock()
    session.execute.return_value.scalars.return_value.all.return_value = ['file1', 'file2']
    files = pytest.run(asyncio=True)(list_user_files)('user_id', None, session)
    assert files == ['file1', 'file2']

@pytest.mark.asyncio
def test_list_user_files_with_folder(monkeypatch):
    session = AsyncMock()
    session.execute.return_value.scalars.return_value.all.return_value = ['file1']
    files = pytest.run(asyncio=True)(list_user_files)('user_id', 'folder_id', session)
    assert files == ['file1']
