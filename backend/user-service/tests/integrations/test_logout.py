import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_logout_success(async_client: AsyncClient):
    reg_data = {"email": "logoutuser@example.com", "username": "logoutuser", "password": "Test1234!"}
    await async_client.post("/register/", json=reg_data)
    login_data = {"email": reg_data["email"], "password": reg_data["password"]}
    resp = await async_client.post("/auth/login", json=login_data)
    tokens = resp.json()
    refresh_token = tokens["refresh_token"]
    resp2 = await async_client.post("/logout/", json={"refresh_token": refresh_token})
    assert resp2.status_code == 200
    assert resp2.json().get("status") == "logged out"

@pytest.mark.asyncio
async def test_logout_invalid_token(async_client: AsyncClient):
    resp = await async_client.post("/logout/", json={"refresh_token": "invalidtoken"})
    assert resp.status_code == 401 or resp.status_code == 400
    assert "Invalid refresh token" in resp.text or "Not authenticated" in resp.text
