import pytest
from unittest.mock import patch

@pytest.mark.asyncio
async def test_upload_file_success(async_client, mock_jwt, mock_minio, mock_scan, mock_stat):
    with patch('upload_file.service.scan_file_for_viruses', mock_scan(True)), \
         patch('upload_file.service.minio_client.put_object', mock_minio()), \
         patch('upload_file.service.update_user_stat', mock_stat()):
        response = await async_client.post(
            '/files/upload',
            files={'upload': ('test.txt', b'data', 'text/plain')},
            headers={'Authorization': f'Bearer {mock_jwt}'}
        )
        assert response.status_code == 200
        assert response.json()['filename'] == 'test.txt'

@pytest.mark.asyncio
async def test_upload_file_virus(async_client, mock_jwt, mock_minio, mock_scan, mock_stat):
    with patch('upload_file.service.scan_file_for_viruses', mock_scan(False)), \
         patch('upload_file.service.minio_client.put_object', mock_minio()), \
         patch('upload_file.service.update_user_stat', mock_stat()):
        response = await async_client.post(
            '/files/upload',
            files={'upload': ('test.txt', b'data', 'text/plain')},
            headers={'Authorization': f'Bearer {mock_jwt}'}
        )
        assert response.status_code == 400
        assert 'вирус' in response.json()['detail'].lower()
