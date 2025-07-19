import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../file-service')))
import os
from minio_utils.minio_client import minio_client

def test_minio_client_config():
    # Проверяем базовые методы клиента
    assert hasattr(minio_client, 'get_object')
    assert hasattr(minio_client, 'put_object')
