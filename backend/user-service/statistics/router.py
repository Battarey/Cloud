from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_async_session
from models.stat_update import StatUpdate
from .service import update_user_stat

router = APIRouter(prefix="/user-stat", tags=["user-stat"])

@router.post("/update", description="Обновление статистики пользователя")
async def update_stat(data: StatUpdate, session: AsyncSession = Depends(get_async_session)):
    return await update_user_stat(data, session)
