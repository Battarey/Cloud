from sqlalchemy.ext.asyncio import AsyncSession
from models.file import File as FileModel
from schemas.file import FileRead
from minio_utils.minio_client import minio_client, MINIO_BUCKET
from statistics.utils import update_user_stat
import uuid
from fastapi import HTTPException
import re
from sqlalchemy.future import select
import io
from virus_scan.service import scan_file_with_clamav

async def scan_file_for_viruses(file_bytes: bytes, filename: str) -> bool:
    result = await scan_file_with_clamav(file_bytes, filename)
    print(f"[file-service] Virus scan result: {result}", flush=True)
    return result.get("clean", False)

async def save_uploaded_file(upload, user_id: str, session: AsyncSession) -> FileRead:
    # Валидация имени файла
    filename = upload.filename
    if not filename or len(filename) > 255 or re.search(r'[\\/:*?"<>|]', filename):
        raise HTTPException(status_code=400, detail="Invalid file name")
    # Запрещённые расширения
    forbidden_exts = {'.exe', '.bat', '.cmd', '.sh'}
    ext = filename.lower().rsplit('.', 1)[-1] if '.' in filename else ''
    if ext and f'.{ext}' in forbidden_exts:
        raise HTTPException(status_code=415, detail="Forbidden file extension")
    # Проверка на дубликат
    dup_result = await session.execute(select(FileModel).where(FileModel.user_id == user_id, FileModel.filename == filename))
    duplicate = dup_result.scalar_one_or_none()
    if duplicate:
        raise HTTPException(status_code=409, detail="File with this name already exists")
    file_id = str(uuid.uuid4())
    storage_key = f"{user_id}/{file_id}/{filename}"
    content = await upload.read()
    # Ограничение размера файла (максимум 1 МБ)
    max_size = 1 * 1024 * 1024
    if len(content) > max_size:
        raise HTTPException(status_code=413, detail="File too large")
    # Проверка на вирусы
    is_clean = await scan_file_for_viruses(content, filename)
    if not is_clean:
        raise HTTPException(status_code=400, detail="Файл заражён вирусом!")
    minio_client.put_object(
        MINIO_BUCKET,
        storage_key,
        data=io.BytesIO(content),
        length=len(content),
        content_type=upload.content_type
    )
    db_file = FileModel(
        id=file_id,
        user_id=user_id,
        filename=filename,
        size=len(content),
        content_type=upload.content_type,
        storage_key=storage_key
    )
    session.add(db_file)
    await session.commit()
    # Обновление статистики пользователя
    await update_user_stat(user_id, "upload", len(content))
    return FileRead(
        id=db_file.id,
        user_id=db_file.user_id,
        filename=db_file.filename,
        size=db_file.size,
        content_type=db_file.content_type,
        created_at=db_file.created_at
    )
