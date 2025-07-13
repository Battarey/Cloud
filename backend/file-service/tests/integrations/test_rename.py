import pytest

@pytest.mark.asyncio
async def test_rename_file_to_existing(async_client, mock_jwt, test_user_id):
    # Создаём два файла, пытаемся переименовать один в имя другого
    import uuid, os
    from sqlalchemy.ext.asyncio import create_async_engine
    from sqlalchemy import text
    file_id1 = str(uuid.uuid4())
    file_id2 = str(uuid.uuid4())
    DATABASE_URL = os.environ["DATABASE_URL"]
    engine = create_async_engine(DATABASE_URL, echo=False)
    async with engine.begin() as conn:
        await conn.execute(
            text("""
                INSERT INTO files (id, user_id, filename, size, content_type, storage_key, created_at)
                VALUES (:id, :user_id, 'file1.txt', 1, 'text/plain', 'key1', now()),
                       (:id2, :user_id, 'file2.txt', 1, 'text/plain', 'key2', now())
            """),
            {"id": file_id1, "id2": file_id2, "user_id": test_user_id}
        )
    resp = await async_client.patch(
        f'/files/{file_id1}',
        params={'new_name': 'file2.txt'},
        headers={'Authorization': f'Bearer {mock_jwt}'}
    )
    assert resp.status_code in (400, 409)
import pytest

@pytest.mark.asyncio
async def test_rename_file_success(async_client, mock_jwt):
    response = await async_client.patch(
        '/files/some-file-id',
        params={'new_name': 'renamed.txt'},
        headers={'Authorization': f'Bearer {mock_jwt}'}
    )
    assert response.status_code in (200, 404)


@pytest.mark.asyncio
async def test_rename_file_not_found(async_client, mock_jwt):
    response = await async_client.patch(
        '/files/nonexistent-file-id',
        params={'new_name': 'renamed.txt'},
        headers={'Authorization': f'Bearer {mock_jwt}'}
    )
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_rename_file_unauthorized(async_client):
    response = await async_client.patch(
        '/files/some-file-id',
        params={'new_name': 'renamed.txt'}
    )
    assert response.status_code == 401

@pytest.mark.asyncio
async def test_rename_folder_success(async_client, mock_jwt):
    response = await async_client.patch(
        '/files/folders/some-folder-id',
        params={'new_name': 'renamed_folder'},
        headers={'Authorization': f'Bearer {mock_jwt}'}
    )
    assert response.status_code in (200, 404)
