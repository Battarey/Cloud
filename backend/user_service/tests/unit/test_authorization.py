import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
import pytest
from authorization.service import login_user, refresh_user_token
from models.user import User
from fastapi import HTTPException
from unittest.mock import AsyncMock
from sqlalchemy.ext.asyncio import AsyncSession
from security.password.password import get_password_hash

@pytest.mark.asyncio
async def test_login_user_success(monkeypatch):
    session = AsyncMock(spec=AsyncSession)
    password = "Test1234!"
    hashed = get_password_hash(password)
    user = User(email="test@example.com", username="testuser", hashed_password=hashed)
    session.execute.return_value.scalar_one_or_none = lambda: user
    # Не нужно мокать verify_password, пусть работает реально
    # Мокаем по месту использования (authorization.service)
    monkeypatch.setattr("authorization.service.create_access_token", lambda d: "access")
    async def fake_create_refresh_token(uid):
        return "refresh"
    monkeypatch.setattr("authorization.service.create_refresh_token", fake_create_refresh_token)
    result = await login_user("test@example.com", password, session)
    assert result["access_token"] == "access"
    assert result["refresh_token"] == "refresh"
    assert result["token_type"] == "bearer"

@pytest.mark.asyncio
async def test_login_user_invalid_credentials(monkeypatch):
    session = AsyncMock(spec=AsyncSession)
    session.execute.return_value.scalar_one_or_none = lambda: None
    with pytest.raises(HTTPException) as exc:
        await login_user("test@example.com", "wrong", session)
    assert exc.value.status_code == 401
    assert "Invalid credentials" in exc.value.detail

@pytest.mark.asyncio
async def test_login_user_wrong_password(monkeypatch):
    session = AsyncMock(spec=AsyncSession)
    password = "Test1234!"
    hashed = get_password_hash(password)
    user = User(email="test@example.com", username="testuser", hashed_password=hashed)
    session.execute.return_value.scalar_one_or_none = lambda: user
    # Не нужно мокать verify_password, пусть работает реально
    with pytest.raises(HTTPException) as exc:
        await login_user("test@example.com", "wrong", session)
    assert exc.value.status_code == 401

@pytest.mark.asyncio
async def test_refresh_user_token_success(monkeypatch):
    # Мокаем redis_client.get и rotate_refresh_token
    async def fake_get(key):
        return "user_id"
    async def fake_rotate_refresh_token(token, user_id):
        return "new_refresh"
    async def fake_delete(key):
        return None
    # Мокаем по месту использования (security.tokens.refresh)
    monkeypatch.setattr("security.tokens.refresh.redis_client.get", fake_get)
    # ВАЖНО: мокать rotate_refresh_token по месту использования в authorization.service
    monkeypatch.setattr("authorization.service.rotate_refresh_token", fake_rotate_refresh_token)
    monkeypatch.setattr("security.tokens.refresh.redis_client.delete", fake_delete)
    monkeypatch.setattr("authorization.service.create_access_token", lambda d: "access")
    result = await refresh_user_token("refresh")
    assert result["access_token"] == "access"
    assert result["refresh_token"] == "new_refresh"
    assert result["token_type"] == "bearer"

@pytest.mark.asyncio
async def test_refresh_user_token_invalid(monkeypatch):
    async def fake_get(key):
        return None
    monkeypatch.setattr("security.tokens.refresh.redis_client.get", fake_get)
    with pytest.raises(HTTPException) as exc:
        await refresh_user_token("badtoken")
    assert exc.value.status_code == 401
    assert "Invalid refresh token" in exc.value.detail
