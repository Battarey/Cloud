import pytest
from minio import Minio
import os, io, uuid
import jwt
from fastapi.testclient import TestClient
import main
from generate_link.router import get_presigned_get_object

@pytest.fixture(scope="module", autouse=True)
def prepare_minio():
    endpoint = os.getenv("MINIO_ENDPOINT", "minio:9000")
    access_key = os.getenv("MINIO_ACCESS_KEY", "minioadmin")
    secret_key = os.getenv("MINIO_SECRET_KEY", "minioadmin")
    bucket = "test-bucket"
    object_name = "test.txt"
    client = Minio(endpoint, access_key=access_key, secret_key=secret_key, secure=False)
    if not client.bucket_exists(bucket):
        client.make_bucket(bucket)
    data = io.BytesIO(b"test data")
    client.put_object(bucket, object_name, data, length=len(b"test data"))
    yield
    # После тестов можно удалить файл и бакет (опционально)
    # client.remove_object(bucket, object_name)
    # client.remove_bucket(bucket)

@pytest.mark.asyncio
async def test_generate_link_success(async_client):
    bucket = "test-bucket"
    object_name = "test.txt"
    response = await async_client.get(
        "/generate-link",
        params={"bucket": bucket, "object_name": object_name}
    )
    assert response.status_code == 200
    data = response.json()
    assert "url" in data
    assert bucket in data["url"]
    assert object_name in data["url"]


@pytest.mark.asyncio
async def test_generate_link_crypto_flow(async_client, mock_jwt_empty):
    """
    Интеграционный тест: upload -> generate-link -> download по ссылке -> проверка расшифровки
    """
    user_id = jwt.decode(mock_jwt_empty, options={"verify_signature": False})["sub"]
    file_content = b"crypto public link test"
    filename = f"crypto_{uuid.uuid4().hex}.txt"
    # Upload
    upload_resp = await async_client.post(
        '/files/upload',
        files={'upload': (filename, file_content, 'text/plain')},
        headers={'Authorization': f'Bearer {mock_jwt_empty}'},
        params={'user_id': user_id}
    )
    assert upload_resp.status_code == 200
    file_id = upload_resp.json()["id"]
    # Получаем публичную ссылку (direct link)
    link_resp = await async_client.get(f"/generate-link/direct/{file_id}/{user_id}")
    assert link_resp.status_code == 200
    # Скачиваем файл по публичной ссылке
    assert link_resp.content == file_content


@pytest.mark.asyncio
async def test_generate_link_nonexistent_bucket(async_client):
    response = await async_client.get(
        "/generate-link",
        params={"bucket": "no-such-bucket", "object_name": "test.txt"}
    )
    assert response.status_code == 500
    assert "Ошибка генерации ссылки" in response.text


@pytest.mark.asyncio
async def test_generate_link_nonexistent_object(async_client):
    response = await async_client.get(
        "/generate-link",
        params={"bucket": "test-bucket", "object_name": "no-such-file.txt"}
    )
    # MinIO всё равно сгенерирует ссылку, даже если объект не существует (до скачивания)
    assert response.status_code == 200
    data = response.json()
    assert "url" in data
    assert "no-such-file.txt" in data["url"]


@pytest.mark.asyncio
@pytest.mark.parametrize("bucket,object_name", [
    ("", "test.txt"),
    ("test-bucket", ""),
    ("", ""),
])
async def test_generate_link_empty_params(async_client, bucket, object_name):
    response = await async_client.get(
        "/generate-link",
        params={"bucket": bucket, "object_name": object_name}
    )
    assert response.status_code in (422, 500)


@pytest.mark.asyncio
async def test_generate_link_missing_params(async_client):
    # Нет bucket
    response = await async_client.get(
        "/generate-link",
        params={"object_name": "test.txt"}
    )
    assert response.status_code == 422
    # Нет object_name
    response = await async_client.get(
        "/generate-link",
        params={"bucket": "test-bucket"}
    )
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_generate_link_long_params(async_client):
    long_bucket = "b" * 256
    long_object = "f" * 1024 + ".txt"
    response = await async_client.get(
        "/generate-link",
        params={"bucket": long_bucket, "object_name": long_object}
    )
    # MinIO может вернуть ошибку, либо API — 500
    assert response.status_code in (500, 200)


@pytest.mark.asyncio
@pytest.mark.parametrize("bucket,object_name", [
    ("test-bucket", "bad/name.txt"),
    ("test-bucket", "bad\\name.txt"),
    ("test-bucket", "<bad>.txt"),
    ("test-bucket", "|bad|.txt"),
])
async def test_generate_link_invalid_chars(async_client, bucket, object_name):
    response = await async_client.get(
        "/generate-link",
        params={"bucket": bucket, "object_name": object_name}
    )
    # MinIO может сгенерировать ссылку, но скачивание не сработает; API не валидирует
    assert response.status_code in (200, 500)

def fake_presigned_get_object(*a, **kw):
    raise Exception("MinIO unavailable")

def test_generate_link_minio_unavailable():
    main.app.dependency_overrides[get_presigned_get_object] = lambda: fake_presigned_get_object
    try:
        client = TestClient(main.app)
        response = client.get(
            "/generate-link",
            params={"bucket": "test-bucket", "object_name": "test.txt"}
        )
        assert response.status_code == 500
        assert "Ошибка генерации ссылки" in response.text
    finally:
        main.app.dependency_overrides = {}

@pytest.mark.asyncio
async def test_generate_link_unique_urls(async_client):
    bucket = "test-bucket"
    obj1 = "test.txt"
    obj2 = "test2.txt"
    resp1 = await async_client.get(
        "/generate-link",
        params={"bucket": bucket, "object_name": obj1}
    )
    resp2 = await async_client.get(
        "/generate-link",
        params={"bucket": bucket, "object_name": obj2}
    )
    assert resp1.status_code == 200
    assert resp2.status_code == 200
    url1 = resp1.json()["url"]
    url2 = resp2.json()["url"]
    assert url1 != url2
