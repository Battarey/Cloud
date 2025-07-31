import pytest
import uuid

@pytest.mark.asyncio
async def test_create_folder_missing_name(async_client, mock_jwt):
    response = await async_client.post(
        '/folders/create',
        headers={'Authorization': f'Bearer {mock_jwt}'}
    )
    assert response.status_code in (400, 422)

@pytest.mark.asyncio
async def test_create_folder_invalid_type(async_client, mock_jwt):
    response = await async_client.post(
        '/folders/create',
        params={'folder_name': 12345},
        headers={'Authorization': f'Bearer {mock_jwt}'}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "12345"

@pytest.mark.asyncio
async def test_create_folder_sql_injection(async_client, mock_jwt):
    response = await async_client.post(
        '/folders/create',
        params={'folder_name': "test'; DROP TABLE files;--"},
        headers={'Authorization': f'Bearer {mock_jwt}'}
    )
    assert response.status_code in (400, 422)

@pytest.mark.asyncio
async def test_create_folder_file_name_conflict(async_client, mock_jwt):
    file_name = f"conflict_{uuid.uuid4().hex}"
    import jwt
    user_id = jwt.decode(mock_jwt, options={"verify_signature": False})["sub"]
    resp_file = await async_client.post(
        '/files/upload',
        files={'upload': (file_name, b'data', 'text/plain')},
        headers={'Authorization': f'Bearer {mock_jwt}'},
        params={'user_id': user_id}
    )
    assert resp_file.status_code == 200
    resp_folder = await async_client.post(
        '/folders/create',
        params={'folder_name': file_name},
        headers={'Authorization': f'Bearer {mock_jwt}'}
    )
    assert resp_folder.status_code == 409

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
