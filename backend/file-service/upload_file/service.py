from sqlalchemy.ext.asyncio import AsyncSession
from models.file import File as FileModel
from schemas.file import FileRead
from minio_utils.minio_client import minio_client, MINIO_BUCKET
from statistics.utils import update_user_stat
import uuid
import httpx
from fastapi import HTTPException
import re
from sqlalchemy.future import select
import io

async def scan_file_for_viruses(file_bytes: bytes) -> bool:
    async with httpx.AsyncClient(timeout=60.0) as client:
        try:
            print("[file-service] Sending file to virus-scan-service...", flush=True)
            response = await client.post(
                "http://virus-scan-service:8000/scan",
                files={"file": ("file", file_bytes)}
            )
            print(f"[file-service] Got response: status={response.status_code}", flush=True)
            print(f"[file-service] Response content: {response.content}", flush=True)
            print(f"[file-service] Response text: {response.text}", flush=True)
            response.raise_for_status()
            result = response.json()
            print(f"[file-service] Virus scan response: {result}", flush=True)
            return result.get("clean", False)
        except Exception as e:
            print(f"[file-service] Virus scan exception: {str(e)}", flush=True)
            if 'response' in locals():
                print(f"[file-service] Response text on exception: {response.text}", flush=True)
            return False

async def save_uploaded_file(upload, user_id: str, session: AsyncSession) -> FileRead:
    # Валидация имени файла
    filename = upload.filename
    if not filename or len(filename) > 255 or re.search(r'[\\/:*?"<>|]', filename):
        raise HTTPException(status_code=400, detail="Invalid file name")
    # Проверка на дубликат
    dup_result = await session.execute(select(FileModel).where(FileModel.user_id == user_id, FileModel.filename == filename))
    duplicate = dup_result.scalar_one_or_none()
    if duplicate:
        raise HTTPException(status_code=409, detail="File with this name already exists")
    file_id = str(uuid.uuid4())
    storage_key = f"{user_id}/{file_id}/{filename}"
    content = await upload.read()
    # Проверка на вирусы
    is_clean = await scan_file_for_viruses(content)
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
