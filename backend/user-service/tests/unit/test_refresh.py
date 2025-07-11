import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
import pytest
from security.tokens.refresh import create_refresh_token, get_user_id_by_refresh, rotate_refresh_token
import security.tokens.refresh as refresh_mod

@pytest.mark.asyncio
async def test_create_refresh_token(monkeypatch):
    async def fake_set(*args, **kwargs):
        return True
    async def fake_lpush(*args, **kwargs):
        return True
    async def fake_ltrim(*args, **kwargs):
        return True
    async def fake_lrange(*args, **kwargs):
        return []
    async def fake_delete(*args, **kwargs):
        return True
    async def fake_setex(*args, **kwargs):
        return True
    monkeypatch.setattr(refresh_mod.redis_client, "set", fake_set)
    monkeypatch.setattr(refresh_mod.redis_client, "lpush", fake_lpush)
    monkeypatch.setattr(refresh_mod.redis_client, "ltrim", fake_ltrim)
    monkeypatch.setattr(refresh_mod.redis_client, "lrange", fake_lrange)
    monkeypatch.setattr(refresh_mod.redis_client, "delete", fake_delete)
    monkeypatch.setattr(refresh_mod.redis_client, "setex", fake_setex)
    token = await create_refresh_token("user_id")
    assert isinstance(token, str)
    assert len(token) > 0

@pytest.mark.asyncio
async def test_rotate_refresh_token(monkeypatch):
    async def fake_revoke(token):
        return None
    async def fake_create_refresh_token(user_id):
        return "new_refresh_token"
    async def fake_delete(key):
        return None
    monkeypatch.setattr("security.tokens.refresh.revoke_refresh_token", fake_revoke)
    monkeypatch.setattr("security.tokens.refresh.create_refresh_token", fake_create_refresh_token)
    monkeypatch.setattr(refresh_mod.redis_client, "delete", fake_delete)
    token = await rotate_refresh_token("oldtoken", "user_id")
    assert isinstance(token, str)

@pytest.mark.asyncio
async def test_get_user_id_by_refresh(monkeypatch):
    async def fake_get(*args, **kwargs):
        return "user_id"
    monkeypatch.setattr(refresh_mod.redis_client, "get", fake_get)
    user_id = await get_user_id_by_refresh("sometoken")
    assert user_id == "user_id"
