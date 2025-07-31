from sqlalchemy.ext.asyncio import AsyncSession
from models.file import File as FileModel
from minio_utils.minio_client import async_get_object, MINIO_BUCKET
from sqlalchemy.future import select
from fastapi import HTTPException
from minio.error import S3Error
import uuid
from security.user_key_utils import get_user_encryption_key
from cryptography.fernet import Fernet

async def get_file_for_download(
    file_id: str,
    user_id: str,
    session: AsyncSession,
    get_object_func=async_get_object
):
    # Проверка корректности UUID
    try:
        file_uuid = uuid.UUID(file_id)
    except (ValueError, TypeError):
        raise HTTPException(status_code=404, detail="File not found")
    result = await session.execute(select(FileModel).where(FileModel.id == file_uuid, FileModel.user_id == user_id))
    file = result.scalar_one_or_none()
    if not file:
        raise HTTPException(status_code=404, detail="File not found")
    try:
        response = await get_object_func(MINIO_BUCKET, file.storage_key)
    except S3Error as e:
        if e.code == "NoSuchKey":
            raise HTTPException(status_code=404, detail="File not found in storage")
        raise HTTPException(status_code=500, detail=f"MinIO error: {e}")
    # Дешифруем файл
    user_key = await get_user_encryption_key(user_id, session)
    fernet = Fernet(user_key)
    encrypted_data = await response.read()
    decrypted_data = fernet.decrypt(encrypted_data)
    # Возвращаем расшифрованные данные и метаданные файла
    return decrypted_data, file
