from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_async_session
from security.jwt import get_current_user
from .service import list_user_files
from schemas.file import FileRead
from typing import List

router = APIRouter(prefix="/files", tags=["files"])

@router.get("/", response_model=List[FileRead])
async def list_files(folder_id: str = None, user_id: str = Depends(get_current_user), session: AsyncSession = Depends(get_async_session)):
    files = await list_user_files(user_id, folder_id, session)
    return files
