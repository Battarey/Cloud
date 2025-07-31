from sqlalchemy.ext.asyncio import AsyncSession
from models.file import File as FileModel
from minio_utils.minio_client import async_remove_object, MINIO_BUCKET
from minio.error import S3Error
from sqlalchemy.future import select
import uuid

async def delete_folder_by_id(
    folder_id: str,
    user_id: str,
    session: AsyncSession,
    remove_object_func=async_remove_object
):
    # Проверка корректности UUID
    try:
        folder_uuid = uuid.UUID(folder_id)
    except (ValueError, TypeError):
        return False
    # Найти папку
    result = await session.execute(select(FileModel).where(FileModel.id == folder_uuid, FileModel.user_id == user_id, FileModel.content_type == 'folder'))
    folder = result.scalar_one_or_none()
    if not folder:
        return False
    # Найти все файлы внутри папки (по storage_key)
    prefix = folder.storage_key
    files_result = await session.execute(select(FileModel).where(FileModel.user_id == user_id, FileModel.storage_key.startswith(prefix)))
    files = files_result.scalars().all()
    # Удалить из MinIO и БД
    try:
        for file in files:
            try:
                await remove_object_func(MINIO_BUCKET, file.storage_key)
            except S3Error as e:
                # Если объект не найден — игнорируем, иначе пробрасываем ошибку
                if e.code != "NoSuchKey":
                    raise
            await session.delete(file)
        await session.delete(folder)
        await session.commit()
        return True
    except S3Error as e:
        # Ошибка MinIO — пробрасываем для возврата 500
        raise RuntimeError(f"MinIO error: {e}")
