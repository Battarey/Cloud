import pytest

@pytest.mark.asyncio
async def test_delete_file_unauthorized(async_client, test_user_id):
    # Создаём файл в базе и Minio
    import uuid, os
    from sqlalchemy.ext.asyncio import create_async_engine
    from sqlalchemy import text
    from tests.integrations.minio_utils import upload_test_file
    file_id = str(uuid.uuid4())
    storage_key = f"test/{file_id}.txt"
    DATABASE_URL = os.environ["DATABASE_URL"]
    engine = create_async_engine(DATABASE_URL, echo=False)
    async with engine.begin() as conn:
        await conn.execute(
            text("""
                INSERT INTO files (id, user_id, filename, size, content_type, storage_key, created_at)
                VALUES (:id, :user_id, 'delete_me.txt', 1, 'text/plain', :storage_key, now())
            """),
            {"id": file_id, "user_id": test_user_id, "storage_key": storage_key}
        )
    await upload_test_file(storage_key)
    response = await async_client.delete(f'/files/{file_id}')
    assert response.status_code == 401
import pytest
import io
import uuid
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text
import os
from tests.integrations.minio_utils import upload_test_file
from minio_utils.minio_client import minio_client, MINIO_BUCKET

@pytest.mark.asyncio
async def test_delete_file_success(async_client, mock_jwt, test_user_id):
    # Создаём файл в базе и загружаем его в Minio
    file_id = str(uuid.uuid4())
    storage_key = f"test/{file_id}.txt"
    DATABASE_URL = os.environ["DATABASE_URL"]
    engine = create_async_engine(DATABASE_URL, echo=False)
    async with engine.begin() as conn:
        await conn.execute(
            text("""
                INSERT INTO files (id, user_id, filename, size, content_type, storage_key, created_at)
                VALUES (:id, :user_id, 'delete_me.txt', 1, 'text/plain', :storage_key, now())
            """),
            {"id": file_id, "user_id": test_user_id, "storage_key": storage_key}
        )
    await upload_test_file(storage_key)
    response = await async_client.delete(
        f'/files/{file_id}',
        headers={'Authorization': f'Bearer {mock_jwt}'}
    )
    assert response.status_code == 200
    assert response.json()['status'] == 'deleted'

    # Очистка бакета происходит автоматически через фикстуру

@pytest.mark.asyncio
async def test_delete_file_not_found(async_client, mock_jwt):
    fake_id = str(uuid.uuid4())
    response = await async_client.delete(
        f'/files/{fake_id}',
        headers={'Authorization': f'Bearer {mock_jwt}'}
    )
    assert response.status_code == 404
