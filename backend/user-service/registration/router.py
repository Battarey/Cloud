from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.user import UserCreate, UserRead
from ..database import get_async_session
from .service import register_user_service

router = APIRouter(prefix="/register", tags=["registration"])

@router.post("/", response_model=UserRead)
async def register_user(user: UserCreate, session: AsyncSession = Depends(get_async_session)):
    return await register_user_service(user, session)
