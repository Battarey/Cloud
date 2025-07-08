from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.file import FileRead
from database import get_async_session
from security.jwt import get_current_user
from .service import save_uploaded_file

router = APIRouter(prefix="/files", tags=["files"])

@router.post("/upload", response_model=FileRead)
async def upload_file(
    upload: UploadFile = File(...),
    user_id: str = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session)
):
    return await save_uploaded_file(upload, user_id, session)
