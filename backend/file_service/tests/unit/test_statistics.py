import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../file-service')))
import pytest
from unittest.mock import patch, AsyncMock
from statistics.utils import update_user_stat

@pytest.mark.asyncio
async def test_update_user_stat_success():
    async_mock_client = AsyncMock()
    async_mock_client.__aenter__.return_value.post = AsyncMock(return_value=AsyncMock(status_code=200, raise_for_status=lambda: None))
    with patch('statistics.utils.httpx.AsyncClient', return_value=async_mock_client):
        await update_user_stat('user_id', 'upload', 123)
        async_mock_client.__aenter__.return_value.post.assert_called_once()

@pytest.mark.asyncio
async def test_update_user_stat_fail():
    async_mock_client = AsyncMock()
    async_mock_client.__aenter__.return_value.post = AsyncMock(side_effect=Exception('fail'))
    with patch('statistics.utils.httpx.AsyncClient', return_value=async_mock_client):
        await update_user_stat('user_id', 'upload', 123)
        async_mock_client.__aenter__.return_value.post.assert_called_once()
