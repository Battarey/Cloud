import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../file-service')))
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from download_file.service import get_file_for_download
from fastapi import HTTPException

@pytest.mark.asyncio
def test_get_file_for_download_success(monkeypatch):
    session = AsyncMock()
    file = MagicMock()
    file.content_type = 'text/plain'
    file.filename = 'test.txt'
    file.storage_key = 'key'
    session.execute.return_value.scalar_one_or_none.return_value = file
    monkeypatch.setattr('download_file.service.minio_client.get_object', MagicMock(return_value=MagicMock()))
    response, result_file = pytest.run(asyncio=True)(get_file_for_download)('file_id', 'user_id', session)
    assert result_file == file
    assert response is not None

@pytest.mark.asyncio
def test_get_file_for_download_not_found():
    session = AsyncMock()
    session.execute.return_value.scalar_one_or_none.return_value = None
    with pytest.raises(HTTPException) as exc:
        pytest.run(asyncio=True)(get_file_for_download)('file_id', 'user_id', session)
    assert exc.value.status_code == 404
