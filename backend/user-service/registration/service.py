from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.user import User
from security.password.password import get_password_hash
from schemas.user import UserCreate
from fastapi import HTTPException

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
    # Возвращаем только нужные поля для UserRead
    return {
        "id": db_user.id,
        "email": db_user.email,
        "username": db_user.username,
        "files_count": db_user.files_count,
        "files_size": db_user.files_size,
        "free_space": db_user.free_space,
    }
