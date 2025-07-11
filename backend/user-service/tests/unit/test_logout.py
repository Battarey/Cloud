import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
import pytest
from logout.service import logout_user_service

@pytest.mark.asyncio
async def test_logout_user_service(monkeypatch):
    called = {}
    async def fake_revoke(token):
        called['token'] = token
        return None
    async def fake_get_user_id_by_refresh(token):
        return "user_id"
    import logout.service as logout_mod
    monkeypatch.setattr(logout_mod, "revoke_refresh_token", fake_revoke)
    from unittest.mock import patch
    with patch("security.tokens.refresh.get_user_id_by_refresh", fake_get_user_id_by_refresh):
        result = await logout_user_service("sometoken")
    assert called.get('token') == "sometoken"
    assert result == {"status": "logged out"}
