from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.user_key import UserKey
from cryptography.fernet import Fernet
import os

async def get_user_encryption_key(user_id: str, session: AsyncSession) -> bytes:
    result = await session.execute(select(UserKey).where(UserKey.user_id == user_id))
    user_key_row = result.scalar_one_or_none()
    if not user_key_row:
        raise Exception(f"Encryption key for user {user_id} not found")
    encrypted_key = user_key_row.encrypted_key.encode()
    master_key = os.getenv("USER_KEY_MASTER")
    if not master_key:
        raise Exception("USER_KEY_MASTER env var not set!")
    fernet = Fernet(master_key.encode())
    user_key = fernet.decrypt(encrypted_key)
    return user_key
