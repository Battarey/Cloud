import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
import pytest
from logout.service import logout_user_service
from unittest.mock import AsyncMock, patch

@pytest.mark.asyncio
async def test_logout_user_service(monkeypatch):
    called = {}
    async def fake_revoke(token):
        called['token'] = token
        return None
    # monkeypatch по реальному объекту
    import logout.service as logout_mod
    monkeypatch.setattr(logout_mod, "revoke_refresh_token", fake_revoke)
    result = await logout_user_service("sometoken")
    assert called.get('token') == "sometoken"
    assert result == {"status": "logged out"}
