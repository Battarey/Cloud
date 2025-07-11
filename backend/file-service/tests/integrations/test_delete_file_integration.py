import pytest
from unittest.mock import patch

@pytest.mark.asyncio
async def test_delete_file_success(async_client, mock_jwt, mock_minio, mock_stat):
    with patch('delete_file.service.minio_client.remove_object', mock_minio()), \
         patch('delete_file.service.update_user_stat', mock_stat()):
        response = await async_client.delete(
            '/files/some-file-id',
            headers={'Authorization': f'Bearer {mock_jwt}'}
        )
        assert response.status_code == 200
        assert response.json()['status'] == 'deleted'

@pytest.mark.asyncio
async def test_delete_file_not_found(async_client, mock_jwt):
    response = await async_client.delete(
        '/files/nonexistent',
        headers={'Authorization': f'Bearer {mock_jwt}'}
    )
    assert response.status_code == 404
