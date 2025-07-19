import pytest
from unittest.mock import AsyncMock, MagicMock
from fastapi import HTTPException

from upload_file.service import save_uploaded_file

@pytest.mark.asyncio
async def test_save_uploaded_file_success(monkeypatch):
    # Мокаем upload
    upload = MagicMock()
    upload.filename = 'test.txt'
    upload.content_type = 'text/plain'
    upload.read = AsyncMock(return_value=b'data')

    # Мокаем session
    session = AsyncMock()
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = None  # Нет дубликата
    session.execute.return_value = mock_result
    session.add = MagicMock()
    session.commit = AsyncMock()

    # Мокаем scan_file_for_viruses
    monkeypatch.setattr('upload_file.service.scan_file_for_viruses', AsyncMock(return_value=True))
    # Мокаем minio_client
    monkeypatch.setattr('upload_file.service.minio_client', MagicMock())
    # Мокаем update_user_stat
    monkeypatch.setattr('upload_file.service.update_user_stat', AsyncMock())

    # Мокаем FileRead
    class DummyFileRead:
        def __init__(self, **kwargs):
            for k, v in kwargs.items():
                setattr(self, k, v)
    monkeypatch.setattr('upload_file.service.FileRead', DummyFileRead)

    result = await save_uploaded_file(upload, 'user_id', session)
    assert isinstance(result, DummyFileRead)
    assert result.filename == 'test.txt'
    assert result.size == len(b'data')

@pytest.mark.asyncio
async def test_save_uploaded_file_duplicate(monkeypatch):
    upload = MagicMock()
    upload.filename = 'test.txt'
    upload.content_type = 'text/plain'
    upload.read = AsyncMock(return_value=b'data')

    session = AsyncMock()
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = True  # Дубликат найден
    session.execute.return_value = mock_result

    monkeypatch.setattr('upload_file.service.scan_file_for_viruses', AsyncMock(return_value=True))
    monkeypatch.setattr('upload_file.service.minio_client', MagicMock())
    monkeypatch.setattr('upload_file.service.update_user_stat', AsyncMock())

    with pytest.raises(HTTPException) as exc:
        await save_uploaded_file(upload, 'user_id', session)
    assert exc.value.status_code == 409

@pytest.mark.asyncio
async def test_save_uploaded_file_invalid_name(monkeypatch):
    upload = MagicMock()
    upload.filename = 'bad|name.txt'
    upload.content_type = 'text/plain'
    upload.read = AsyncMock(return_value=b'data')

    session = AsyncMock()

    with pytest.raises(HTTPException) as exc:
        await save_uploaded_file(upload, 'user_id', session)
    assert exc.value.status_code == 400

@pytest.mark.asyncio
async def test_save_uploaded_file_virus(monkeypatch):
    upload = MagicMock()
    upload.filename = 'test.txt'
    upload.content_type = 'text/plain'
    upload.read = AsyncMock(return_value=b'data')

    session = AsyncMock()
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = None
    session.execute.return_value = mock_result

    monkeypatch.setattr('upload_file.service.scan_file_for_viruses', AsyncMock(return_value=False))
    monkeypatch.setattr('upload_file.service.minio_client', MagicMock())
    monkeypatch.setattr('upload_file.service.update_user_stat', AsyncMock())

    with pytest.raises(HTTPException) as exc:
        await save_uploaded_file(upload, 'user_id', session)
    assert exc.value.status_code == 400
    assert "вирус" in exc.value.detail.lower()