import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../file-service')))
import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from upload_file.service import save_uploaded_file, scan_file_for_viruses
from schemas.file import FileRead
from fastapi import HTTPException

@pytest.mark.asyncio
def test_scan_file_for_viruses_clean():
    with patch('upload_file.service.httpx.AsyncClient') as mock_client:
        mock_instance = mock_client.return_value.__aenter__.return_value
        mock_instance.post.return_value.json.return_value = {"clean": True}
        mock_instance.post.return_value.raise_for_status = lambda: None
        result = pytest.run(asyncio=True)(scan_file_for_viruses)(b'data')
        assert result

@pytest.mark.asyncio
def test_scan_file_for_viruses_infected():
    with patch('upload_file.service.httpx.AsyncClient') as mock_client:
        mock_instance = mock_client.return_value.__aenter__.return_value
        mock_instance.post.return_value.json.return_value = {"clean": False}
        mock_instance.post.return_value.raise_for_status = lambda: None
        result = pytest.run(asyncio=True)(scan_file_for_viruses)(b'data')
        assert not result

@pytest.mark.asyncio
def test_save_uploaded_file_virus(monkeypatch):
    upload = MagicMock()
    upload.filename = 'test.txt'
    upload.content_type = 'text/plain'
    upload.read = AsyncMock(return_value=b'data')
    session = AsyncMock()
    monkeypatch.setattr('upload_file.service.scan_file_for_viruses', AsyncMock(return_value=False))
    with pytest.raises(HTTPException) as exc:
        pytest.run(asyncio=True)(save_uploaded_file)(upload, 'user_id', session)
    assert exc.value.status_code == 400
    assert "вирус" in exc.value.detail.lower()

@pytest.mark.asyncio
def test_save_uploaded_file_success(monkeypatch):
    upload = MagicMock()
    upload.filename = 'test.txt'
    upload.content_type = 'text/plain'
    upload.read = AsyncMock(return_value=b'data')
    session = AsyncMock()
    monkeypatch.setattr('upload_file.service.scan_file_for_viruses', AsyncMock(return_value=True))
    monkeypatch.setattr('upload_file.service.minio_client.put_object', MagicMock())
    monkeypatch.setattr('upload_file.service.update_user_stat', AsyncMock())
    monkeypatch.setattr('upload_file.service.FileModel', MagicMock())
    session.add = AsyncMock()
    session.commit = AsyncMock()
    session.refresh = AsyncMock()
    result = pytest.run(asyncio=True)(save_uploaded_file)(upload, 'user_id', session)
    assert isinstance(result, FileRead)
