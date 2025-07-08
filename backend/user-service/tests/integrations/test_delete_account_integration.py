import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_delete_account_success(async_client: AsyncClient):
    reg_data = {"email": "deluser@example.com", "username": "deluser", "password": "Test1234!"}
    reg_resp = await async_client.post("/register/", json=reg_data)
    login_data = {"email": reg_data["email"], "password": reg_data["password"]}
    login_resp = await async_client.post("/auth/login", json=login_data)
    access_token = login_resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}
    resp = await async_client.delete("/delete-account/", headers=headers)
    assert resp.status_code == 200
    assert resp.json().get("status") == "deleted"

@pytest.mark.asyncio
async def test_delete_account_unauthorized(async_client: AsyncClient):
    resp = await async_client.delete("/delete-account/")
    assert resp.status_code == 401 or resp.status_code == 403
    assert "Not authenticated" in resp.text or "credentials" in resp.text
