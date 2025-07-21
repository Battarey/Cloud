import pytest
import uuid

@pytest.mark.asyncio
async def test_upload_file_success(async_client, mock_jwt_empty):
    import jwt
    user_id = jwt.decode(mock_jwt_empty, options={"verify_signature": False})["sub"]
    unique_name = f"test_{uuid.uuid4().hex}.txt"
    response = await async_client.post(
        '/files/upload',
        files={'upload': (unique_name, b'data', 'text/plain')},
        headers={'Authorization': f'Bearer {mock_jwt_empty}'},
        params={'user_id': user_id}
    )
    assert response.status_code == 200
    assert response.json()['filename'] == unique_name
    assert response.json()['size'] == len(b'data')

@pytest.mark.asyncio
async def test_upload_file_forbidden_ext(async_client, mock_jwt_empty):
    import jwt
    user_id = jwt.decode(mock_jwt_empty, options={"verify_signature": False})["sub"]
    response = await async_client.post(
        '/files/upload',
        files={'upload': ('test.exe', b'data', 'application/octet-stream')},
        headers={'Authorization': f'Bearer {mock_jwt_empty}'},
        params={'user_id': user_id}
    )
    assert response.status_code == 415

@pytest.mark.asyncio
async def test_upload_file_duplicate(async_client, mock_jwt_empty):
    import jwt
    user_id = jwt.decode(mock_jwt_empty, options={"verify_signature": False})["sub"]
    name = f"dup_{uuid.uuid4().hex}.txt"
    response1 = await async_client.post(
        '/files/upload',
        files={'upload': (name, b'data', 'text/plain')},
        headers={'Authorization': f'Bearer {mock_jwt_empty}'},
        params={'user_id': user_id}
    )
    assert response1.status_code == 200
    response2 = await async_client.post(
        '/files/upload',
        files={'upload': (name, b'data', 'text/plain')},
        headers={'Authorization': f'Bearer {mock_jwt_empty}'},
        params={'user_id': user_id}
    )
    assert response2.status_code == 409

@pytest.mark.asyncio
async def test_upload_file_too_large(async_client, mock_jwt_empty):
    import jwt
    user_id = jwt.decode(mock_jwt_empty, options={"verify_signature": False})["sub"]
    big_data = b'a' * (2 * 1024 * 1024)  # 2 МБ
    response = await async_client.post(
        '/files/upload',
        files={'upload': ('big.txt', big_data, 'text/plain')},
        headers={'Authorization': f'Bearer {mock_jwt_empty}'},
        params={'user_id': user_id}
    )
    assert response.status_code == 413

@pytest.mark.asyncio
async def test_upload_file_invalid_symbols(async_client, mock_jwt_empty):
    import jwt
    user_id = jwt.decode(mock_jwt_empty, options={"verify_signature": False})["sub"]
    response = await async_client.post(
        '/files/upload',
        files={'upload': ('bad|name.txt', b'data', 'text/plain')},
        headers={'Authorization': f'Bearer {mock_jwt_empty}'},
        params={'user_id': user_id}
    )
    assert response.status_code == 400

@pytest.mark.asyncio
async def test_upload_file_empty_content(async_client, mock_jwt_empty):
    import jwt
    user_id = jwt.decode(mock_jwt_empty, options={"verify_signature": False})["sub"]
    response = await async_client.post(
        '/files/upload',
        files={'upload': ('empty.txt', b'', 'text/plain')},
        headers={'Authorization': f'Bearer {mock_jwt_empty}'},
        params={'user_id': user_id}
    )
    assert response.status_code in (200, 400, 422)

@pytest.mark.asyncio
async def test_upload_file_no_extension(async_client, mock_jwt_empty):
    import jwt
    user_id = jwt.decode(mock_jwt_empty, options={"verify_signature": False})["sub"]
    response = await async_client.post(
        '/files/upload',
        files={'upload': ('noextension', b'data', 'text/plain')},
        headers={'Authorization': f'Bearer {mock_jwt_empty}'},
        params={'user_id': user_id}
    )
    assert response.status_code in (200, 422)

@pytest.mark.asyncio
async def test_upload_file_double_extension(async_client, mock_jwt_empty):
    import jwt
    user_id = jwt.decode(mock_jwt_empty, options={"verify_signature": False})["sub"]
    response = await async_client.post(
        '/files/upload',
        files={'upload': ('file.exe.txt', b'data', 'text/plain')},
        headers={'Authorization': f'Bearer {mock_jwt_empty}'},
        params={'user_id': user_id}
    )
    assert response.status_code in (200, 422)

@pytest.mark.asyncio
async def test_upload_file_too_long_name(async_client, mock_jwt_empty):
    import jwt
    user_id = jwt.decode(mock_jwt_empty, options={"verify_signature": False})["sub"]
    long_name = 'a' * 256 + '.txt'
    response = await async_client.post(
        '/files/upload',
        files={'upload': (long_name, b'data', 'text/plain')},
        headers={'Authorization': f'Bearer {mock_jwt_empty}'},
        params={'user_id': user_id}
    )
    assert response.status_code in (400, 422)

@pytest.mark.asyncio
async def test_upload_file_empty_name(async_client, mock_jwt_empty):
    response = await async_client.post(
        '/files/upload',
        files={'upload': ('', b'data', 'text/plain')},
        headers={'Authorization': f'Bearer {mock_jwt_empty}'}
    )
    assert response.status_code in (400, 422)

@pytest.mark.asyncio
async def test_upload_file_missing_upload(async_client, mock_jwt_empty):
    import jwt
    user_id = jwt.decode(mock_jwt_empty, options={"verify_signature": False})["sub"]
    response = await async_client.post(
        '/files/upload',
        headers={'Authorization': f'Bearer {mock_jwt_empty}'},
        params={'user_id': user_id}
    )
    assert response.status_code == 422

@pytest.mark.asyncio
async def test_upload_file_invalid_token(async_client):
    response = await async_client.post(
        '/files/upload',
        files={'upload': ('test.txt', b'data', 'text/plain')},
        headers={'Authorization': 'Bearer invalidtoken'}
    )
    assert response.status_code == 401

@pytest.mark.asyncio
async def test_upload_file_unauthorized(async_client):
    response = await async_client.post(
        '/files/upload',
        files={'upload': ('test.txt', b'data', 'text/plain')}
    )
    assert response.status_code == 401

@pytest.mark.asyncio
async def test_upload_file_invalid_headers(async_client, mock_jwt_empty):
    response = await async_client.post(
        '/files/upload',
        files={'upload': ('file.txt', b'data', 'text/plain')},
        headers={'Authorization': f'Bearer {mock_jwt_empty}', 'Content-Type': 'application/json'}
    )
    assert response.status_code in (400, 415, 422, 200)

@pytest.mark.asyncio
async def test_upload_file_wrong_content_type(async_client, mock_jwt_empty):
    import jwt
    user_id = jwt.decode(mock_jwt_empty, options={"verify_signature": False})["sub"]
    response = await async_client.post(
        '/files/upload',
        files={'upload': ('test.txt', b'data', 'application/unknown')},
        headers={'Authorization': f'Bearer {mock_jwt_empty}'},
        params={'user_id': user_id}
    )
    assert response.status_code in (200, 422)
    import jwt
    user_id = jwt.decode(mock_jwt_empty, options={"verify_signature": False})["sub"]
    filename = f"chunked_{uuid.uuid4().hex}.bin"
    upload_id = str(uuid.uuid4())
    total_chunks = 3
    chunk_size = 1024 * 1024  # 1 МБ
    # Инициализация chunked upload
    for i in range(1, total_chunks + 1):
        chunk_data = b'a' * chunk_size
        response = await async_client.post(
            '/files/upload/chunk',
            files={'chunk': (filename, chunk_data, 'application/octet-stream')},
            headers={'Authorization': f'Bearer {mock_jwt_empty}'},
            params={
                'chunk_number': i,
                'total_chunks': total_chunks,
                'upload_id': upload_id,
                'filename': filename,
                'user_id': user_id
            }
        )
        if i < total_chunks:
            assert response.status_code == 200
            assert response.json()['status'] == 'chunk uploaded'
        else:
            assert response.status_code == 200
            assert response.json()['filename'] == filename
            assert response.json()['size'] == chunk_size * total_chunks
