import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../file-service')))
import pytest
from unittest.mock import AsyncMock, MagicMock
from rename.service import rename_file, rename_folder
from fastapi import HTTPException
import uuid

@pytest.mark.asyncio
async def test_rename_file_success(monkeypatch):
    session = AsyncMock()
    file = MagicMock()
    # Первый вызов - поиск по id, возвращаем файл; второй - проверка дубликата, возвращаем None
    call_count = {'count': 0}
    def execute_side_effect(*args, **kwargs):
        # Первый вызов — проверка дубликата, возвращаем None (нет дубликата)
        # Второй вызов — поиск по id, возвращаем файл
        if call_count['count'] == 0:
            call_count['count'] += 1
            return MagicMock(scalar_one_or_none=MagicMock(return_value=None))
        else:
            return MagicMock(scalar_one_or_none=MagicMock(return_value=file))
    session.execute.side_effect = execute_side_effect
    session.commit = AsyncMock()
    session.refresh = AsyncMock()
    result = await rename_file(str(uuid.uuid4()), str(uuid.uuid4()), 'new.txt', session)
    assert result == file

@pytest.mark.asyncio
async def test_rename_file_not_found():
    session = AsyncMock()
    # Первый вызов - поиск по id, возвращаем None
    session.execute.return_value = MagicMock(scalar_one_or_none=MagicMock(return_value=None))
    with pytest.raises(HTTPException) as exc:
        await rename_file(str(uuid.uuid4()), str(uuid.uuid4()), 'new.txt', session)
    assert exc.value.status_code == 404

@pytest.mark.asyncio
async def test_rename_folder_success(monkeypatch):
    session = AsyncMock()
    folder = MagicMock()
    # Первый вызов - поиск по id, возвращаем папку; второй - проверка дубликата, возвращаем None
    call_count = {'count': 0}
    def execute_side_effect(*args, **kwargs):
        # Первый вызов — проверка дубликата, возвращаем None (нет дубликата)
        # Второй вызов — поиск по id, возвращаем папку
        if call_count['count'] == 0:
            call_count['count'] += 1
            return MagicMock(scalar_one_or_none=MagicMock(return_value=None))
        else:
            return MagicMock(scalar_one_or_none=MagicMock(return_value=folder))
    session.execute.side_effect = execute_side_effect
    session.commit = AsyncMock()
    session.refresh = AsyncMock()
    result = await rename_folder(str(uuid.uuid4()), str(uuid.uuid4()), 'new_folder', session)
    assert result == folder

@pytest.mark.asyncio
async def test_rename_folder_not_found():
    session = AsyncMock()
    session.execute.return_value = MagicMock(scalar_one_or_none=MagicMock(return_value=None))
    with pytest.raises(HTTPException) as exc:
        await rename_folder(str(uuid.uuid4()), str(uuid.uuid4()), 'new_folder', session)
    assert exc.value.status_code == 404
