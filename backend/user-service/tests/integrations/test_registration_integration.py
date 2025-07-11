import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_register_user_success(async_client: AsyncClient):
    data = {
        "email": "testuser1@example.com",
        "username": "testuser1",
        "password": "Test1234!"
    }
    resp = await async_client.post("/register/", json=data)
    assert resp.status_code == 200
    result = resp.json()
    assert result["email"] == data["email"]
    assert result["username"] == data["username"]
    assert result["files_count"] == 0
    assert result["files_size"] == 0
    assert result["free_space"] > 0

@pytest.mark.asyncio
async def test_register_user_duplicate(async_client: AsyncClient):
    data = {
        "email": "testuser2@example.com",
        "username": "testuser2",
        "password": "Test1234!"
    }
    resp1 = await async_client.post("/register/", json=data)
    assert resp1.status_code == 200
    resp2 = await async_client.post("/register/", json=data)
    assert resp2.status_code == 400
    assert "already registered" in resp2.text

@pytest.mark.asyncio
@pytest.mark.parametrize("email,username,password,expected_error", [
    ("bademail", "user", "Test1234!", "value is not a valid email address"),
    ("test@example.com", "us", "Test1234!", "String should have at least 3 characters"),
    ("test@example.com", "user@name", "Test1234!", "String should match pattern"),
    ("test@example.com", "username", "short", "String should have at least 8 characters"),
    ("test@example.com", "username", "nouppercase1!", "Пароль должен содержать хотя бы одну заглавную букву"),
    ("test@example.com", "username", "NOLOWERCASE1!", "Пароль должен содержать хотя бы одну строчную букву"),
    ("test@example.com", "username", "NoNumber!", "Пароль должен содержать хотя бы одну цифру"),
    ("test@example.com", "username", "NoNumber1", "Пароль должен содержать хотя бы один спецсимвол"),
])
async def test_register_user_schema_validation(async_client: AsyncClient, email, username, password, expected_error):
    data = {"email": email, "username": username, "password": password}
    resp = await async_client.post("/register/", json=data)
    assert resp.status_code == 422 or resp.status_code == 400
    assert expected_error in resp.text

@pytest.mark.asyncio
async def test_register_user_sql_injection(async_client: AsyncClient):
    data = {
        "email": "testinject@example.com' OR 1=1;--",
        "username": "injectuser",
        "password": "Test1234!"
    }
    resp = await async_client.post("/register/", json=data)
    assert resp.status_code == 422 or resp.status_code == 400
    assert "valid email" in resp.text or "value is not a valid email address" in resp.text

    data2 = {
        "email": "inject2@example.com",
        "username": "user' OR 1=1;--",
        "password": "Test1234!"
    }
    resp2 = await async_client.post("/register/", json=data2)
    assert resp2.status_code == 422 or resp2.status_code == 400
    assert "pattern" in resp2.text or "match" in resp2.text
