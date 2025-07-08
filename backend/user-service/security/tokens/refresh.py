import os
import uuid
import redis.asyncio as redis
from datetime import timedelta

REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
REFRESH_EXPIRE_DAYS = 7
REFRESH_LIMIT = 3

redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

async def create_refresh_token(user_id: str) -> str:
    token = str(uuid.uuid4())
    expire = timedelta(days=REFRESH_EXPIRE_DAYS)
    key = f"refresh_list:{user_id}"
    await redis_client.lpush(key, token)
    await redis_client.ltrim(key, 0, REFRESH_LIMIT - 1)
    tokens = await redis_client.lrange(key, 0, -1)
    if len(tokens) > REFRESH_LIMIT:
        for old_token in tokens[REFRESH_LIMIT:]:
            await redis_client.delete(f"refresh:{old_token}")
    await redis_client.setex(f"refresh:{token}", int(expire.total_seconds()), user_id)
    return token

async def get_user_id_by_refresh(token: str) -> str | None:
    return await redis_client.get(f"refresh:{token}")

async def revoke_refresh_token(token: str):
    await redis_client.delete(f"refresh:{token}")

async def rotate_refresh_token(old_token: str, user_id: str) -> str:
    # Проверяем, не был ли токен уже отозван (использован)
    exists = await redis_client.exists(f"refresh:{old_token}")
    if not exists:
        raise Exception("Refresh token already used or revoked")
    await revoke_refresh_token(old_token)
    return await create_refresh_token(user_id)
