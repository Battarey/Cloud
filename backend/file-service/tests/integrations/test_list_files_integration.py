import pytest

@pytest.mark.asyncio
async def test_list_files_success(async_client, mock_jwt):
    response = await async_client.get(
        '/files/',
        headers={'Authorization': f'Bearer {mock_jwt}'}
    )
    assert response.status_code == 200
    assert isinstance(response.json(), list)
