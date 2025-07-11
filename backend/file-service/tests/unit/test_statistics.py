import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../file-service')))
import pytest
from unittest.mock import patch, AsyncMock
from statistics.utils import update_user_stat

@pytest.mark.asyncio
def test_update_user_stat_success():
    with patch('statistics.utils.httpx.AsyncClient') as mock_client:
        mock_instance = mock_client.return_value.__aenter__.return_value
        mock_instance.post = AsyncMock(return_value=AsyncMock(status_code=200, raise_for_status=lambda: None))
        pytest.run(asyncio=True)(update_user_stat)('user_id', 'upload', 123)
        mock_instance.post.assert_called_once()

@pytest.mark.asyncio
def test_update_user_stat_fail():
    with patch('statistics.utils.httpx.AsyncClient') as mock_client:
        mock_instance = mock_client.return_value.__aenter__.return_value
        mock_instance.post = AsyncMock(side_effect=Exception('fail'))
        pytest.run(asyncio=True)(update_user_stat)('user_id', 'upload', 123)
        mock_instance.post.assert_called_once()
