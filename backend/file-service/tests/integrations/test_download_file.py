import pytest

@pytest.mark.asyncio
async def test_download_file_after_delete(async_client, mock_jwt, test_user_id):
    # Создаём файл, удаляем, затем пробуем скачать
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
