import pytest

@pytest.mark.asyncio
async def test_list_files_success(async_client, mock_jwt):
    response = await async_client.get(
        '/files/',
        headers={'Authorization': f'Bearer {mock_jwt}'}
    )
    assert response.status_code == 200
    assert isinstance(response.json(), list)


@pytest.mark.asyncio
async def test_list_files_unauthorized(async_client):
    response = await async_client.get('/files/')
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_list_files_empty(async_client, mock_jwt_empty):
    # Для нового пользователя список должен быть пустым
    response = await async_client.get(
        '/files/',
        headers={'Authorization': f'Bearer {mock_jwt_empty}'}
    )
    assert response.status_code == 200
    assert response.json() == []
