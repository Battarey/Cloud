from fastapi import APIRouter, UploadFile, File, Depends, Query, HTTPException
import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.file import FileRead
from database import get_async_session
from security.jwt import get_current_user
from .service import save_uploaded_file

router = APIRouter(prefix="/files", tags=["files"])

@router.post("/upload", response_model=FileRead, description="Загрузка файла пользователем")
async def upload_file(
    upload: UploadFile = File(...),
    user_id: str = Query(...),
    session: AsyncSession = Depends(get_async_session),
    current_user: str = Depends(get_current_user)
):
    # Проверка авторизации: user_id должен совпадать с current_user
    if user_id != current_user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    # Строгая валидация UUID
    try:
        uuid.UUID(user_id)
    except Exception:
        raise HTTPException(status_code=422, detail="Invalid user_id (must be UUID)")
    return await save_uploaded_file(upload, user_id, session)
