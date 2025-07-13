import pytest

@pytest.mark.asyncio
async def test_create_folder_empty_name(async_client, mock_jwt):
    response = await async_client.post(
        '/folders/create',
        params={'folder_name': ''},
        headers={'Authorization': f'Bearer {mock_jwt}'}
    )
    assert response.status_code in (400, 422)

@pytest.mark.asyncio
async def test_create_folder_invalid_chars(async_client, mock_jwt):
    response = await async_client.post(
        '/folders/create',
        params={'folder_name': 'bad/name'},
        headers={'Authorization': f'Bearer {mock_jwt}'}
    )
    assert response.status_code in (400, 422)

@pytest.mark.asyncio
async def test_create_folder_long_name(async_client, mock_jwt):
    long_name = 'a' * 300
    response = await async_client.post(
        '/folders/create',
        params={'folder_name': long_name},
        headers={'Authorization': f'Bearer {mock_jwt}'}
    )
    assert response.status_code in (400, 422)
import pytest

@pytest.mark.asyncio
async def test_create_folder_success(async_client, mock_jwt):
    response = await async_client.post(
        '/folders/create',
        params={'folder_name': 'new_folder'},
        headers={'Authorization': f'Bearer {mock_jwt}'}
    )
    assert response.status_code == 200
    assert response.json()['status'] == 'created'


@pytest.mark.asyncio
async def test_create_folder_unauthorized(async_client):
    response = await async_client.post(
        '/folders/create',
        params={'folder_name': 'unauth_folder'}
    )
    assert response.status_code == 401

@pytest.mark.asyncio
async def test_create_folder_duplicate(async_client, mock_jwt):
    # Сначала создаём папку
    response1 = await async_client.post(
        '/folders/create',
        params={'folder_name': 'dup_folder'},
        headers={'Authorization': f'Bearer {mock_jwt}'}
    )
    assert response1.status_code == 200
    # Пытаемся создать с тем же именем
    response2 = await async_client.post(
        '/folders/create',
        params={'folder_name': 'dup_folder'},
        headers={'Authorization': f'Bearer {mock_jwt}'}
    )
    assert response2.status_code in (400, 409)
