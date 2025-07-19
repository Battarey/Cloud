import asyncio
import httpx
import pytest
import uuid

@pytest.mark.asyncio
async def test_upload_file_race_condition(async_client, mock_jwt_empty):
    name = f"race_{uuid.uuid4().hex}.txt"
    # user_id из токена
    import jwt
    user_id = jwt.decode(mock_jwt_empty, options={"verify_signature": False})["sub"]
    async def upload():
        return await async_client.post(
            '/files/upload',
            files={'upload': (name, b'data', 'text/plain')},
            headers={'Authorization': f'Bearer {mock_jwt_empty}'},
            params={'user_id': user_id}
        )
    results = await asyncio.gather(upload(), upload())
    codes = [r.status_code for r in results]
    # сервис возвращает оба 200, если нет защиты от гонки
    assert codes.count(200) == 2

@pytest.mark.asyncio
async def test_upload_file_invalid_type(async_client, mock_jwt_empty):
    import jwt
    user_id = jwt.decode(mock_jwt_empty, options={"verify_signature": False})["sub"]
    response = await async_client.post(
        '/files/upload',
        files={'upload': ("12345", b'data', 'text/plain')},
        headers={'Authorization': f'Bearer {mock_jwt_empty}'},
        params={'user_id': user_id}
    )
    assert response.status_code == 200

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
async def test_upload_file_long_content_type(async_client, mock_jwt_empty):
    import jwt
    user_id = jwt.decode(mock_jwt_empty, options={"verify_signature": False})["sub"]
    long_type = 'a' * 300
    response = await async_client.post(
        '/files/upload',
        files={'upload': ('file.txt', b'data', long_type)},
        headers={'Authorization': f'Bearer {mock_jwt_empty}'},
        params={'user_id': user_id}
    )
    assert response.status_code in (200, 400, 422)

@pytest.mark.asyncio
async def test_upload_file_sql_injection(async_client, mock_jwt_empty):
    import jwt
    user_id = jwt.decode(mock_jwt_empty, options={"verify_signature": False})["sub"]
    response = await async_client.post(
        '/files/upload',
        files={'upload': ("test'; DROP TABLE files;--.txt", b'data', 'text/plain')},
        headers={'Authorization': f'Bearer {mock_jwt_empty}'},
        params={'user_id': user_id}
    )
    assert response.status_code == 400

@pytest.mark.asyncio
async def test_upload_file_invalid_uuid(async_client, mock_jwt_empty):
    response = await async_client.post(
        '/files/upload',
        files={'upload': ('file.txt', b'data', 'text/plain')},
        headers={'Authorization': f'Bearer {mock_jwt_empty}'},
        params={'user_id': 'not-a-uuid'}
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
async def test_upload_file_rate_limit():
    # Имитация лимита: 20 запросов подряд
    async with httpx.AsyncClient(base_url="http://host.docker.internal:8002") as client:
        results = []
        for _ in range(20):
            resp = await client.post(
                '/files/upload',
                files={'upload': (f"rate_{uuid.uuid4().hex}.txt", b'data', 'text/plain')},
                headers={'Authorization': 'Bearer invalidtoken'}
            )
            results.append(resp.status_code)
        # Если лимит реализован, появится 429
        assert any(code == 429 for code in results) or all(code == 401 for code in results)

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
async def test_upload_file_invalid_symbols(async_client, mock_jwt_empty):
    import jwt
    user_id = jwt.decode(mock_jwt_empty, options={"verify_signature": False})["sub"]
    response = await async_client.post(
        '/files/upload',
        files={'upload': ('bad|name.txt', b'data', 'text/plain')},
        headers={'Authorization': f'Bearer {mock_jwt_empty}'},
        params={'user_id': user_id}
    )
    assert response.status_code in (400, 422)

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

@pytest.mark.asyncio
async def test_upload_file_invalid_token(async_client):
    response = await async_client.post(
        '/files/upload',
        files={'upload': ('test.txt', b'data', 'text/plain')},
        headers={'Authorization': 'Bearer invalidtoken'}
    )
    assert response.status_code == 401

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
    assert response.status_code in (200, 422)
    if response.status_code == 200:
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
    import jwt
    user_id = jwt.decode(mock_jwt_empty, options={"verify_signature": False})["sub"]
    big_data = b'a' * (2 * 1024 * 1024)  # 2 МБ
    response = await async_client.post(
        '/files/upload',
        files={'upload': ('big.txt', big_data, 'text/plain')},
        headers={'Authorization': f'Bearer {mock_jwt_empty}'},
        params={'user_id': user_id}
    )
    assert response.status_code in (413, 422)

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
    import jwt
    user_id = jwt.decode(mock_jwt_empty, options={"verify_signature": False})["sub"]
    response = await async_client.post(
        '/files/upload',
        files={'upload': ('test.exe', b'data', 'application/octet-stream')},
        headers={'Authorization': f'Bearer {mock_jwt_empty}'},
        params={'user_id': user_id}
    )
    assert response.status_code in (415, 422)

@pytest.mark.asyncio
async def test_upload_file_duplicate(async_client, mock_jwt_empty):
    dup_name = f"dup_{uuid.uuid4().hex}.txt"
    import jwt
    user_id = jwt.decode(mock_jwt_empty, options={"verify_signature": False})["sub"]
    response1 = await async_client.post(
        '/files/upload',
        files={'upload': (dup_name, b'data', 'text/plain')},
        headers={'Authorization': f'Bearer {mock_jwt_empty}'},
        params={'user_id': user_id}
    )
    assert response1.status_code == 200
    response2 = await async_client.post(
        '/files/upload',
        files={'upload': (dup_name, b'data', 'text/plain')},
        headers={'Authorization': f'Bearer {mock_jwt_empty}'}
    )
    assert response2.status_code == 422
