import pytest
from httpx import AsyncClient
from main import app
from unittest.mock import patch

@pytest.mark.asyncio
async def test_create_folder_success(async_client, mock_jwt):
    response = await async_client.post(
        '/folders/create',
        params={'folder_name': 'new_folder'},
        headers={'Authorization': f'Bearer {mock_jwt}'}
    )
    assert response.status_code == 200
    assert response.json()['status'] == 'created'
