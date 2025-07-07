import pytest
from httpx import AsyncClient
import uuid

@pytest.mark.asyncio
async def test_update_user_stat_upload(async_client: AsyncClient):
    reg_data = {"email": "statuser@example.com", "username": "statuser", "password": "Test1234!"}
    reg_resp = await async_client.post("/register/", json=reg_data)
    user_id = reg_resp.json()["id"]
    data = {"user_id": user_id, "action": "upload", "file_size": 123}
    resp = await async_client.post("/user-stat/update", json=data)
    assert resp.status_code == 200
    result = resp.json()
    assert result["status"] == "ok"
    assert result["files_count"] == 1
    assert result["files_size"] == 123

@pytest.mark.asyncio
async def test_update_user_stat_delete(async_client: AsyncClient):
    reg_data = {"email": "statuser2@example.com", "username": "statuser2", "password": "Test1234!"}
    reg_resp = await async_client.post("/register/", json=reg_data)
    user_id = reg_resp.json()["id"]
    await async_client.post("/user-stat/update", json={"user_id": user_id, "action": "upload", "file_size": 100})
    resp = await async_client.post("/user-stat/update", json={"user_id": user_id, "action": "delete", "file_size": 100})
    assert resp.status_code == 200
    result = resp.json()
    assert result["files_count"] == 0
    assert result["files_size"] == 0

@pytest.mark.asyncio
async def test_update_user_stat_user_not_found(async_client: AsyncClient):
    data = {"user_id": str(uuid.uuid4()), "action": "upload", "file_size": 100}
    resp = await async_client.post("/user-stat/update", json=data)
    assert resp.status_code == 404
    assert "User not found" in resp.text

@pytest.mark.asyncio
async def test_update_user_stat_invalid_action(async_client: AsyncClient):
    reg_data = {"email": "statuser3@example.com", "username": "statuser3", "password": "Test1234!"}
    reg_resp = await async_client.post("/register/", json=reg_data)
    user_id = reg_resp.json()["id"]
    data = {"user_id": user_id, "action": "invalid", "file_size": 100}
    resp = await async_client.post("/user-stat/update", json=data)
    assert resp.status_code == 400
    assert "Invalid action" in resp.text

@pytest.mark.asyncio
async def test_update_user_stat_negative_file_size(async_client: AsyncClient):
    reg_data = {"email": "statuser4@example.com", "username": "statuser4", "password": "Test1234!"}
    reg_resp = await async_client.post("/register/", json=reg_data)
    user_id = reg_resp.json()["id"]
    data = {"user_id": user_id, "action": "upload", "file_size": -100}
    resp = await async_client.post("/user-stat/update", json=data)
    assert resp.status_code == 422 or resp.status_code == 400
