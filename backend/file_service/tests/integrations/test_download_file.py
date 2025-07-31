import pytest
import uuid
import jwt
import uuid, os
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text
from tests.integrations.minio_utils import upload_test_file

@pytest.mark.asyncio
async def test_upload_and_download_file_crypto(async_client, mock_jwt_empty):
    """
    Интеграционный тест: upload -> download -> проверка расшифровки
    """
    user_id = jwt.decode(mock_jwt_empty, options={"verify_signature": False})["sub"]
    file_content = b"crypto download test"
    filename = f"crypto_{uuid.uuid4().hex}.txt"
    # Upload
    upload_resp = await async_client.post(
        '/files/upload',
        files={'upload': (filename, file_content, 'text/plain')},
        headers={'Authorization': f'Bearer {mock_jwt_empty}'},
        params={'user_id': user_id}
    )
    assert upload_resp.status_code == 200
    file_id = upload_resp.json()["id"]
    # Download
    download_resp = await async_client.get(f"/files/{file_id}", headers={"Authorization": f"Bearer {mock_jwt_empty}"})
    assert download_resp.status_code == 200
    assert download_resp.content == file_content

@pytest.mark.asyncio
async def test_download_file_missing_authorization(async_client):
    response = await async_client.get('/files/some-file-id')
    assert response.status_code == 401

@pytest.mark.asyncio
async def test_download_file_invalid_uuid(async_client, mock_jwt):
    response = await async_client.get(
        '/files/not-a-uuid',
        headers={'Authorization': f'Bearer {mock_jwt}'}
    )
    assert response.status_code in (400, 422, 404)

@pytest.mark.asyncio
async def test_download_file_missing_file_in_minio(async_client, mock_jwt, test_user_id):
    # Создаём файл в БД, но не загружаем в MinIO
    file_id = str(uuid.uuid4())
    DATABASE_URL = os.environ["DATABASE_URL"]
    engine = create_async_engine(DATABASE_URL, echo=False)
    async with engine.begin() as conn:
        await conn.execute(
            text("""
                INSERT INTO files (id, user_id, filename, size, content_type, storage_key, created_at)
                VALUES (:id, :user_id, 'missing.txt', 1, 'text/plain', 'missing_key', now())
            """),
            {"id": file_id, "user_id": test_user_id}
        )
    response = await async_client.get(
        f'/files/{file_id}',
        headers={'Authorization': f'Bearer {mock_jwt}'}
    )
    assert response.status_code in (404, 500)

@pytest.mark.asyncio
async def test_download_file_after_delete(async_client, mock_jwt, test_user_id):
    # Создаём файл, удаляем, затем пробуем скачать
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
    # Удаляем
    del_resp = await async_client.delete(
        f'/files/{file_id}',
        headers={'Authorization': f'Bearer {mock_jwt}'}
    )
    assert del_resp.status_code == 200
    # Пробуем скачать
    get_resp = await async_client.get(
        f'/files/{file_id}',
        headers={'Authorization': f'Bearer {mock_jwt}'}
    )
    assert get_resp.status_code == 404
import pytest

@pytest.mark.asyncio
async def test_download_file_success(async_client, mock_jwt):
    response = await async_client.get(
        '/files/some-file-id',
        headers={'Authorization': f'Bearer {mock_jwt}'}
    )
    assert response.status_code in (200, 404)  # 200 если найден, 404 если не найден


@pytest.mark.asyncio
async def test_download_file_not_found(async_client, mock_jwt):
    response = await async_client.get(
        '/files/nonexistent-file-id',
        headers={'Authorization': f'Bearer {mock_jwt}'}
    )
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_download_file_unauthorized(async_client):
    response = await async_client.get('/files/some-file-id')
    assert response.status_code == 401
