from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.user import User
from security.password.password import get_password_hash
from schemas.user import UserCreate
from fastapi import HTTPException
from models.user_key import UserKey
from cryptography.fernet import Fernet
import os

async def register_user_service(user: UserCreate, session: AsyncSession) -> User:
    result = await session.execute(select(User).where((User.email == user.email) | (User.username == user.username)))
    existing_user = result.scalar_one_or_none()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email or username already registered")
    hashed_password = get_password_hash(user.password)
    db_user = User(email=user.email, username=user.username, hashed_password=hashed_password)
    session.add(db_user)
    await session.commit()
    await session.refresh(db_user)

    # Генерация ключа для пользователя (32 байта)
    user_key = Fernet.generate_key()  # Fernet использует 32 байта
    # Шифруем ключ с помощью master-key из переменной окружения
    master_key = os.getenv("USER_KEY_MASTER")
    if not master_key:
        raise Exception("USER_KEY_MASTER env var not set!")
    fernet = Fernet(master_key.encode())
    encrypted_key = fernet.encrypt(user_key)
    # Сохраняем зашифрованный ключ в таблицу user_keys
    db_user_key = UserKey(user_id=db_user.id, encrypted_key=encrypted_key.decode())
    session.add(db_user_key)
    await session.commit()

    # Возвращаем только нужные поля для UserRead
    return {
        "id": db_user.id,
        "email": db_user.email,
        "username": db_user.username,
        "files_count": db_user.files_count,
        "files_size": db_user.files_size,
        "free_space": db_user.free_space,
    }
