from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from ..database import get_async_session
from security.tokens.jwt import get_current_user
from models.user import User
from .service import delete_account_service

router = APIRouter(prefix="/delete-account", tags=["delete-account"])

@router.delete("/")
async def delete_account(current_user: User = Depends(get_current_user), session: AsyncSession = Depends(get_async_session)):
    return await delete_account_service(current_user, session)
