from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_async_session
from security.jwt import get_current_user
from .service import create_folder, FolderCreateError

router = APIRouter(prefix="/folders", tags=["folders"])


import re

@router.post("/create", description="Создание новой папки пользователем")
async def create_folder_endpoint(folder_name: str, user_id: str = Depends(get_current_user), session: AsyncSession = Depends(get_async_session)):
    try:
        folder = await create_folder(user_id, folder_name, session)
    except FolderCreateError as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    return {"id": folder.id, "name": folder.filename, "status": "created"}
