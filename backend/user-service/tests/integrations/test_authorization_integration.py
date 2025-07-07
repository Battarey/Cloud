import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_login_success(async_client: AsyncClient):
    reg_data = {"email": "authuser@example.com", "username": "authuser", "password": "Test1234!"}
    await async_client.post("/register/", json=reg_data)
    login_data = {"email": reg_data["email"], "password": reg_data["password"]}
    resp = await async_client.post("/auth/login", json=login_data)
    assert resp.status_code == 200
    result = resp.json()
    assert "access_token" in result
    assert "refresh_token" in result
    assert result["token_type"] == "bearer"

@pytest.mark.asyncio
async def test_login_wrong_password(async_client: AsyncClient):
    reg_data = {"email": "wrongpass@example.com", "username": "wrongpass", "password": "Test1234!"}
    await async_client.post("/register/", json=reg_data)
    login_data = {"email": reg_data["email"], "password": "WrongPass123!"}
    resp = await async_client.post("/auth/login", json=login_data)
    assert resp.status_code == 401 or resp.status_code == 400
    assert "Invalid credentials" in resp.text

@pytest.mark.asyncio
async def test_login_sql_injection(async_client: AsyncClient):
    reg_data = {"email": "sqlinj@example.com", "username": "sqlinj", "password": "Test1234!"}
    await async_client.post("/register/", json=reg_data)
    login_data = {"email": "sqlinj@example.com' OR 1=1;--", "password": "Test1234!"}
    resp = await async_client.post("/auth/login", json=login_data)
    assert resp.status_code == 422 or resp.status_code == 401 or resp.status_code == 400

@pytest.mark.asyncio
async def test_refresh_success(async_client: AsyncClient):
    reg_data = {"email": "refreshuser@example.com", "username": "refreshuser", "password": "Test1234!"}
    await async_client.post("/register/", json=reg_data)
    login_data = {"email": reg_data["email"], "password": reg_data["password"]}
    resp = await async_client.post("/auth/login", json=login_data)
    tokens = resp.json()
    refresh_token = tokens["refresh_token"]
    resp2 = await async_client.post("/auth/refresh", json={"refresh_token": refresh_token})
    assert resp2.status_code == 200
    result = resp2.json()
    assert "access_token" in result
    assert "refresh_token" in result
    assert result["token_type"] == "bearer"

@pytest.mark.asyncio
async def test_refresh_invalid_token(async_client: AsyncClient):
    resp = await async_client.post("/auth/refresh", json={"refresh_token": "invalidtoken"})
    assert resp.status_code == 401 or resp.status_code == 400
    assert "Invalid refresh token" in resp.text or "Not authenticated" in resp.text

@pytest.mark.asyncio
async def test_refresh_reuse_token(async_client: AsyncClient):
    reg_data = {"email": "reuseuser@example.com", "username": "reuseuser", "password": "Test1234!"}
    await async_client.post("/register/", json=reg_data)
    login_data = {"email": reg_data["email"], "password": reg_data["password"]}
    resp = await async_client.post("/auth/login", json=login_data)
    tokens = resp.json()
    refresh_token = tokens["refresh_token"]
    resp2 = await async_client.post("/auth/refresh", json={"refresh_token": refresh_token})
    assert resp2.status_code == 200
    resp3 = await async_client.post("/auth/refresh", json={"refresh_token": refresh_token})
    assert resp3.status_code == 401 or resp3.status_code == 400
    assert "Invalid refresh token" in resp3.text or "Not authenticated" in resp3.text
