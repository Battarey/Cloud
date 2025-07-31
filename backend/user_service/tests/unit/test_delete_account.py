import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
import pytest
from delete_account.service import delete_account_service
from models.user import User
from unittest.mock import AsyncMock
from sqlalchemy.ext.asyncio import AsyncSession

@pytest.mark.asyncio
async def test_delete_account_service():
    session = AsyncMock(spec=AsyncSession)
    user = User(email="test@example.com", username="testuser", hashed_password="hashed")
    session.delete = AsyncMock()
    session.commit = AsyncMock()
    result = await delete_account_service(user, session)
    session.delete.assert_awaited_with(user)
    session.commit.assert_awaited()
    assert result == {"status": "deleted"}
