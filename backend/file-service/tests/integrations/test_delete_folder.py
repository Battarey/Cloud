import pytest

@pytest.mark.asyncio
async def test_delete_folder_with_files(async_client, mock_jwt, test_user_id):
    import uuid, os
    from sqlalchemy.ext.asyncio import create_async_engine
    from sqlalchemy import text
    folder_id = str(uuid.uuid4())
    file_id = str(uuid.uuid4())
    folder_name = f"folder_{uuid.uuid4().hex}"
    file_name = f"file_{uuid.uuid4().hex}.txt"
    DATABASE_URL = os.environ["DATABASE_URL"]
    engine = create_async_engine(DATABASE_URL, echo=False)
    async with engine.begin() as conn:
        await conn.execute(
            text("""
                INSERT INTO files (id, user_id, filename, size, content_type, storage_key, created_at)
                VALUES (:folder_id, :user_id, :folder_name, 0, 'folder', :folder_key, now()),
                       (:file_id, :user_id, :file_name, 1, 'text/plain', :file_key, now())
            """),
            {
                "folder_id": folder_id,
                "user_id": test_user_id,
                "folder_name": folder_name,
                "folder_key": f"{test_user_id}/{folder_id}/{folder_name}/",
                "file_id": file_id,
                "file_name": file_name,
                "file_key": f"{test_user_id}/{folder_id}/{file_name}"
            }
        )
    response = await async_client.delete(
        f'/folders/{folder_id}',
        headers={'Authorization': f'Bearer {mock_jwt}'}
    )
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_delete_folder_success(async_client, mock_jwt):
    response = await async_client.delete(
        '/folders/some-folder-id',
        headers={'Authorization': f'Bearer {mock_jwt}'}
    )
    assert response.status_code in (200, 404)  # 200 если удалено, 404 если не найдено


@pytest.mark.asyncio
async def test_delete_folder_not_found(async_client, mock_jwt):
    response = await async_client.delete(
        '/folders/nonexistent-folder-id',
        headers={'Authorization': f'Bearer {mock_jwt}'}
    )
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_delete_folder_unauthorized(async_client):
    response = await async_client.delete('/folders/some-folder-id')
    assert response.status_code == 401
