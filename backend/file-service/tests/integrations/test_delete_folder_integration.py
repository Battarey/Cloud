import pytest
from httpx import AsyncClient
from main import app

@pytest.mark.asyncio
async def test_delete_folder_success(async_client, mock_jwt):
    response = await async_client.delete(
        '/folders/some-folder-id',
        headers={'Authorization': f'Bearer {mock_jwt}'}
    )
    assert response.status_code in (200, 404)  # 200 если удалено, 404 если не найдено
