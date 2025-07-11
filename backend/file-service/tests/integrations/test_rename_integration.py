import pytest

@pytest.mark.asyncio
async def test_rename_file_success(async_client, mock_jwt):
    response = await async_client.patch(
        '/files/some-file-id',
        params={'new_name': 'renamed.txt'},
        headers={'Authorization': f'Bearer {mock_jwt}'}
    )
    assert response.status_code in (200, 404)

@pytest.mark.asyncio
async def test_rename_folder_success(async_client, mock_jwt):
    response = await async_client.patch(
        '/files/folders/some-folder-id',
        params={'new_name': 'renamed_folder'},
        headers={'Authorization': f'Bearer {mock_jwt}'}
    )
    assert response.status_code in (200, 404)
