import pytest
import uuid

@pytest.mark.asyncio
async def test_upload_file_success(async_client, mock_jwt_empty):
    unique_name = f"test_{uuid.uuid4().hex}.txt"
    response = await async_client.post(
        '/files/upload',
        files={'upload': (unique_name, b'data', 'text/plain')},
        headers={'Authorization': f'Bearer {mock_jwt_empty}'}
    )
    assert response.status_code == 200
    assert response.json()['filename'] == unique_name

@pytest.mark.asyncio
async def test_upload_file_unauthorized(async_client):
    response = await async_client.post(
        '/files/upload',
        files={'upload': ('test.txt', b'data', 'text/plain')}
    )
    assert response.status_code == 401

@pytest.mark.asyncio
async def test_upload_file_too_large(async_client, mock_jwt_empty):
    big_data = b'a' * (2 * 1024 * 1024)  # 2 МБ
    response = await async_client.post(
        '/files/upload',
        files={'upload': ('big.txt', big_data, 'text/plain')},
        headers={'Authorization': f'Bearer {mock_jwt_empty}'}
    )
    assert response.status_code == 413

@pytest.mark.asyncio
async def test_upload_file_empty_name(async_client, mock_jwt_empty):
    response = await async_client.post(
        '/files/upload',
        files={'upload': ('', b'data', 'text/plain')},
        headers={'Authorization': f'Bearer {mock_jwt_empty}'}
    )
    assert response.status_code in (400, 422)

@pytest.mark.asyncio
async def test_upload_file_forbidden_ext(async_client, mock_jwt_empty):
    response = await async_client.post(
        '/files/upload',
        files={'upload': ('test.exe', b'data', 'application/octet-stream')},
        headers={'Authorization': f'Bearer {mock_jwt_empty}'}
    )
    assert response.status_code == 415

@pytest.mark.asyncio
async def test_upload_file_duplicate(async_client, mock_jwt_empty):
    dup_name = f"dup_{uuid.uuid4().hex}.txt"
    response1 = await async_client.post(
        '/files/upload',
        files={'upload': (dup_name, b'data', 'text/plain')},
        headers={'Authorization': f'Bearer {mock_jwt_empty}'}
    )
    assert response1.status_code == 200
    response2 = await async_client.post(
        '/files/upload',
        files={'upload': (dup_name, b'data', 'text/plain')},
        headers={'Authorization': f'Bearer {mock_jwt_empty}'}
    )
    assert response2.status_code == 409
