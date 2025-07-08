from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_async_session
from security.jwt import get_current_user
from .service import rename_file
from schemas.file import FileRead

router = APIRouter(prefix="/files", tags=["files"])

@router.patch("/{file_id}", response_model=FileRead)
async def rename_file_endpoint(file_id: str, new_name: str, user_id: str = Depends(get_current_user), session: AsyncSession = Depends(get_async_session)):
    file = await rename_file(file_id, user_id, new_name, session)
    return file
