from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.user import User
from ..security.password.password import verify_password
from ..security.tokens.jwt import create_access_token, get_current_user
from ..security.tokens.refresh import create_refresh_token, get_user_id_by_refresh, rotate_refresh_token
from fastapi import HTTPException, Depends

async def login_user(email: str, password: str, session: AsyncSession):
    result = await session.execute(select(User).where(User.email == email))
    user = result.scalar_one_or_none()
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token = create_access_token({"sub": str(user.id)})
    refresh_token = await create_refresh_token(str(user.id))
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}

async def refresh_user_token(refresh_token: str):
    user_id = await get_user_id_by_refresh(refresh_token)
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid refresh token")
    new_refresh_token = await rotate_refresh_token(refresh_token, user_id)
    access_token = create_access_token({"sub": user_id})
    return {"access_token": access_token, "refresh_token": new_refresh_token, "token_type": "bearer"}

async def get_me_user(current_user: User = Depends(get_current_user)):
    return current_user
