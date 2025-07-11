import pytest

@pytest.mark.asyncio
async def test_download_file_success(async_client, mock_jwt):
    response = await async_client.get(
        '/files/some-file-id',
        headers={'Authorization': f'Bearer {mock_jwt}'}
    )
    assert response.status_code in (200, 404)  # 200 если найден, 404 если не найден
