from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_async_session
from security.jwt import get_current_user
from .service import rename_file, rename_folder
from schemas.file import FileRead

router = APIRouter(prefix="/files", tags=["files"])

@router.patch("/{file_id}", response_model=FileRead)
async def rename_file_endpoint(file_id: str, new_name: str, user_id: str = Depends(get_current_user), session: AsyncSession = Depends(get_async_session)):
    try:
        file = await rename_file(file_id, user_id, new_name, session)
    except HTTPException as e:
        raise e
    return file

@router.patch("/folders/{folder_id}", response_model=FileRead)
async def rename_folder_endpoint(folder_id: str, new_name: str, user_id: str = Depends(get_current_user), session: AsyncSession = Depends(get_async_session)):
    try:
        folder = await rename_folder(folder_id, user_id, new_name, session)
    except HTTPException as e:
        raise e
    return folder
