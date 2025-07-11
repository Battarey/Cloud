import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../file-service')))
import os
from minio_utils.minio_client import minio_client

def test_minio_client_config():
    assert minio_client._endpoint_url == os.getenv("MINIO_ENDPOINT")
    assert minio_client._access_key == os.getenv("MINIO_ACCESS_KEY")
    assert minio_client._secret_key == os.getenv("MINIO_SECRET_KEY")
