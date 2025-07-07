import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_register_sql_injection_email(async_client: AsyncClient):
    data = {"email": "test@example.com' OR 1=1;--", "username": "sqluser", "password": "Test1234!"}
    resp = await async_client.post("/register/", json=data)
    assert resp.status_code == 422 or resp.status_code == 400
    assert "valid email" in resp.text or "value is not a valid email address" in resp.text

@pytest.mark.asyncio
async def test_login_sql_injection_email(async_client: AsyncClient):
    data = {"email": "test@example.com' OR 1=1;--", "password": "Test1234!"}
    resp = await async_client.post("/auth/login", json=data)
    assert resp.status_code == 422 or resp.status_code == 401 or resp.status_code == 400

@pytest.mark.asyncio
async def test_update_stat_sql_injection_user_id(async_client: AsyncClient):
    data = {"user_id": "' OR 1=1;--", "action": "upload", "file_size": 100}
    resp = await async_client.post("/user-stat/update", json=data)
    assert resp.status_code == 422 or resp.status_code == 400

@pytest.mark.asyncio
async def test_access_foreign_user_stat(async_client: AsyncClient):
    reg_data = {"email": "secuser1@example.com", "username": "secuser1", "password": "Test1234!"}
    reg_resp = await async_client.post("/register/", json=reg_data)
    user_id = reg_resp.json()["id"]
    fake_id = "00000000-0000-0000-0000-000000000000"
    data = {"user_id": fake_id, "action": "upload", "file_size": 100}
    resp = await async_client.post("/user-stat/update", json=data)
    assert resp.status_code == 404 or resp.status_code == 403

@pytest.mark.asyncio
async def test_me_unauthorized(async_client: AsyncClient):
    resp = await async_client.get("/auth/me")
    assert resp.status_code == 401 or resp.status_code == 403
    assert "Not authenticated" in resp.text or "credentials" in resp.text
