import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../file-service')))
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from delete_file.service import delete_file_by_id

@pytest.mark.asyncio
def test_delete_file_by_id_success(monkeypatch):
    session = AsyncMock()
    file = MagicMock()
    session.execute.return_value.scalar_one_or_none.return_value = file
    monkeypatch.setattr('delete_file.service.minio_client.remove_object', MagicMock())
    monkeypatch.setattr('delete_file.service.update_user_stat', AsyncMock())
    session.delete = AsyncMock()
    session.commit = AsyncMock()
    result = pytest.run(asyncio=True)(delete_file_by_id)('file_id', 'user_id', session)
    assert result is True

@pytest.mark.asyncio
def test_delete_file_by_id_not_found():
    session = AsyncMock()
    session.execute.return_value.scalar_one_or_none.return_value = None
    result = pytest.run(asyncio=True)(delete_file_by_id)('file_id', 'user_id', session)
    assert result is False
