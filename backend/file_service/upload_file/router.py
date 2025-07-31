from fastapi import APIRouter, UploadFile, File, Depends, Query, HTTPException
import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.file import FileRead
from database import get_async_session
from security.jwt import get_current_user
import re
from .service import save_uploaded_file, save_file_chunk, assemble_chunks_if_complete

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


# Chunked upload endpoint
@router.post("/upload/chunk", description="Загрузка части большого файла (chunked upload)")
async def upload_file_chunk(
    chunk: UploadFile = File(...),
    chunk_number: int = Query(..., ge=1, description="Номер чанка (начиная с 1)"),
    total_chunks: int = Query(..., description="Общее количество чанков"),
    upload_id: str = Query(..., description="ID загрузки (UUID)"),
    filename: str = Query(..., description="Имя файла"),
    user_id: str = Query(...),
    session: AsyncSession = Depends(get_async_session),
    current_user: str = Depends(get_current_user)
):
    if user_id != current_user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    try:
        uuid.UUID(user_id)
        uuid.UUID(upload_id)
    except Exception:
        raise HTTPException(status_code=422, detail="Invalid UUID")
    if not filename or re.search(r"[\\/<>:\"|?*]", filename):
        raise HTTPException(status_code=400, detail="Invalid filename: forbidden characters")
    await save_file_chunk(chunk, chunk_number, total_chunks, upload_id, filename, user_id)
    # Если это последний чанк — собираем файл
    if chunk_number == total_chunks:
        return await assemble_chunks_if_complete(upload_id, filename, user_id, session)
    return {"status": "chunk uploaded", "chunk_number": chunk_number}
