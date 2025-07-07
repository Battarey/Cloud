import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from registration.service import register_user_service
from models.user import User
from schemas.user import UserCreate
from fastapi import HTTPException
from unittest.mock import AsyncMock

@pytest.mark.asyncio
async def test_register_user_success(monkeypatch):
    session = AsyncMock(spec=AsyncSession)
    session.execute.return_value.scalar_one_or_none = lambda: None
    session.add = AsyncMock()
    session.commit = AsyncMock()
    session.refresh = AsyncMock()
    user_data = UserCreate(email="test@example.com", username="testuser", password="Test1234!")
    # monkeypatch get_password_hash to return a static hash
    monkeypatch.setattr("security.password.password.get_password_hash", lambda x: "hashed")
    result = await register_user_service(user_data, session)
    assert result.email == user_data.email
    assert result.username == user_data.username
    assert hasattr(result, "hashed_password")

@pytest.mark.asyncio
async def test_register_user_already_exists(monkeypatch):
    session = AsyncMock(spec=AsyncSession)
    session.execute.return_value.scalar_one_or_none = lambda: User()
    user_data = UserCreate(email="test@example.com", username="testuser", password="Test1234!")
    with pytest.raises(HTTPException) as exc:
        await register_user_service(user_data, session)
    assert exc.value.status_code == 400
    assert "already registered" in exc.value.detail

    @pytest.mark.parametrize(
        "email,username,password,expected_error",
        [
            ("bademail", "user", "Test1234!", "value is not a valid email address"),
            ("test@example.com", "us", "Test1234!", "String should have at least 3 characters"),
            ("test@example.com", "user@name", "Test1234!", "String should match pattern"),
            ("test@example.com", "username", "short", "String should have at least 8 characters"),
            ("test@example.com", "username", "nouppercase1!", "Пароль должен содержать хотя бы одну заглавную букву"),
            ("test@example.com", "username", "NOLOWERCASE1!", "Пароль должен содержать хотя бы одну строчную букву"),
            ("test@example.com", "username", "NoNumber!", "Пароль должен содержать хотя бы одну цифру"),
            ("test@example.com", "username", "NoNumber1", "Пароль должен содержать хотя бы один спецсимвол"),
        ]
    )
    def test_register_user_schema_validation(email, username, password, expected_error):
        with pytest.raises(Exception) as exc:
            UserCreate(email=email, username=username, password=password)
        assert expected_error in str(exc.value)
