from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_async_session
from pydantic import BaseModel, EmailStr, Field
from .service import login_user, refresh_user_token, get_me_user
from security.tokens.jwt import get_current_user
from models.user import User

class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=128)

class RefreshRequest(BaseModel):
    refresh_token: str

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login", description="Вход пользователя по email и паролю")
async def login(data: LoginRequest, session: AsyncSession = Depends(get_async_session)):
    return await login_user(data.email, data.password, session)

@router.post("/refresh", description="Обновление access-токена по refresh-токену")
async def refresh_token(data: RefreshRequest):
    return await refresh_user_token(data.refresh_token)

@router.get("/me", description="Получение профиля текущего пользователя")
async def get_me(current_user: User = Depends(get_current_user)):
    return await get_me_user(current_user)
