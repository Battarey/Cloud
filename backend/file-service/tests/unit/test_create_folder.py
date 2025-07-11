import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../file-service')))
import pytest
from unittest.mock import AsyncMock, MagicMock
from create_folder.service import create_folder

@pytest.mark.asyncio
def test_create_folder(monkeypatch):
    session = AsyncMock()
    session.add = AsyncMock()
    session.commit = AsyncMock()
    session.refresh = AsyncMock()
    monkeypatch.setattr('create_folder.service.FileModel', MagicMock())
    folder = pytest.run(asyncio=True)(create_folder)('user_id', 'folder_name', session)
    assert folder is not None
    assert hasattr(folder, 'filename')
