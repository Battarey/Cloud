import os
import httpx

AUTH_SERVICE_URL = os.getenv("AUTH_SERVICE_URL", "http://auth-service:8001")

async def update_user_stat(user_id: str, action: str, file_size: int):
    url = f"{AUTH_SERVICE_URL}/user-stat/update"
    data = {
        "user_id": user_id,
        "action": action,
        "file_size": file_size
    }
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.post(url, json=data, timeout=5)
            resp.raise_for_status()
        except Exception as e:
            # Можно логировать ошибку, но не прерывать основной процесс
            print(f"[WARN] Failed to update user stat: {e}")
