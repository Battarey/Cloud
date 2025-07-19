import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../file-service')))
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from download_file.service import get_file_for_download
from fastapi import HTTPException

@pytest.mark.asyncio
async def test_get_file_for_download_success(monkeypatch):
    session = AsyncMock()
    class DummyFile:
        content_type = 'text/plain'
        filename = 'test.txt'
        storage_key = 'key'
    dummy_file = DummyFile()
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = dummy_file
    session.execute.return_value = mock_result
    monkeypatch.setattr('download_file.service.minio_client.get_object', MagicMock(return_value=MagicMock()))
    import uuid
    response, result_file = await get_file_for_download(str(uuid.uuid4()), 'user_id', session)
    assert result_file == dummy_file
    assert response is not None

@pytest.mark.asyncio
async def test_get_file_for_download_not_found():
    session = AsyncMock()
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = None
    session.execute.return_value = mock_result
    import uuid
    with pytest.raises(HTTPException) as exc:
        await get_file_for_download(str(uuid.uuid4()), 'user_id', session)
    assert exc.value.status_code == 404
