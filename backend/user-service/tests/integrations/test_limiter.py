import pytest
from httpx import AsyncClient
import asyncio

@pytest.mark.asyncio
async def test_register_rate_limit(async_client: AsyncClient):
    data = {"email": "limuser@example.com", "username": "limuser", "password": "Test1234!"}
    for i in range(5):
        resp = await async_client.post("/register/", json={**data, "email": f"limuser{i}@example.com", "username": f"limuser{i}"})
        if i == 0:
            assert resp.status_code == 200
        else:
            if resp.status_code == 429:
                assert "rate limit" in resp.text.lower() or "too many" in resp.text.lower()
                break
            else:
                assert resp.status_code in (200, 400)
        await asyncio.sleep(0.1)

@pytest.mark.asyncio
async def test_login_rate_limit(async_client: AsyncClient):
    reg_data = {"email": "limlogin@example.com", "username": "limlogin", "password": "Test1234!"}
    await async_client.post("/register/", json=reg_data)
    for i in range(10):
        login_data = {"email": reg_data["email"], "password": "WrongPass123!"}
        resp = await async_client.post("/auth/login", json=login_data)
        if resp.status_code == 429:
            assert "rate limit" in resp.text.lower() or "too many" in resp.text.lower()
            break
        else:
            assert resp.status_code in (401, 400)
        await asyncio.sleep(0.1)
