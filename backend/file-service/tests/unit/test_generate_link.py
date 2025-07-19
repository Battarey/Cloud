import pytest
from fastapi import HTTPException
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../file-service')))
from generate_link.service import generate_presigned_url

class DummyMinioClient:
    def presigned_get_object(self, bucket, object_name, expires):
        if object_name == "fail.txt":
            raise Exception("fail")
        return f"https://dummy/{bucket}/{object_name}?expires={expires.total_seconds()}"

@pytest.fixture(autouse=True)
def patch_minio(monkeypatch):
    monkeypatch.setattr("generate_link.service.minio_client", DummyMinioClient())

@pytest.mark.asyncio
async def test_generate_presigned_url_success():
    url = await generate_presigned_url("test-bucket", "test.txt", expires=10800)
    assert url.startswith("https://dummy/test-bucket/test.txt")
    assert "expires=10800.0" in url

@pytest.mark.asyncio
async def test_generate_presigned_url_error():
    with pytest.raises(HTTPException):
        await generate_presigned_url("bucket", "fail.txt", expires=10800)
