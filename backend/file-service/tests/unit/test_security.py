import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../file-service')))
import pytest
from security.jwt import create_access_token, get_current_user
from fastapi import HTTPException
from jose import jwt as jose_jwt
import os

def test_create_access_token():
    token = create_access_token({"sub": "user_id"})
    assert isinstance(token, str)
    payload = jose_jwt.decode(token, os.getenv("SECRET_KEY", "secret"), algorithms=["HS256"])
    assert payload["sub"] == "user_id"

@pytest.mark.asyncio
async def test_get_current_user_valid(monkeypatch):
    token = create_access_token({"sub": "user_id"})
    class DummyDepends:
        def __init__(self, value): self.value = value
        def __call__(self, *a, **k): return self.value
    monkeypatch.setattr('security.jwt.oauth2_scheme', DummyDepends(token))
    user_id = await get_current_user(token)
    assert user_id == "user_id"

@pytest.mark.asyncio
async def test_get_current_user_invalid():
    with pytest.raises(HTTPException):
        await get_current_user("invalid.token")
