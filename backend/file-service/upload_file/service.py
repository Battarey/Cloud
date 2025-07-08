from sqlalchemy.ext.asyncio import AsyncSession
from models.file import File as FileModel
from schemas.file import FileRead
from minio.minio_client import minio_client, MINIO_BUCKET
from statistics.utils import update_user_stat
import uuid

async def save_uploaded_file(upload, user_id: str, session: AsyncSession) -> FileRead:
    file_id = str(uuid.uuid4())
    storage_key = f"{user_id}/{file_id}/{upload.filename}"
    content = await upload.read()
    minio_client.put_object(
        MINIO_BUCKET,
        storage_key,
        data=content,
        length=len(content),
        content_type=upload.content_type
    )
    db_file = FileModel(
        id=file_id,
        user_id=user_id,
        filename=upload.filename,
        size=len(content),
        content_type=upload.content_type,
        storage_key=storage_key
    )
    session.add(db_file)
    await session.commit()
    await session.refresh(db_file)
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
