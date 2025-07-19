import pytest
from minio import Minio
import os

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
    import io
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
