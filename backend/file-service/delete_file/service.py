from sqlalchemy.ext.asyncio import AsyncSession
from models.file import File as FileModel
from minio.minio_client import minio_client, MINIO_BUCKET
from sqlalchemy.future import select
from statistics.utils import update_user_stat

async def delete_file_by_id(file_id: str, user_id: str, session: AsyncSession):
    result = await session.execute(select(FileModel).where(FileModel.id == file_id, FileModel.user_id == user_id))
    file = result.scalar_one_or_none()
    if not file:
        return False
    # Удаляем из MinIO
    minio_client.remove_object(MINIO_BUCKET, file.storage_key)
    # Удаляем из БД
    await session.delete(file)
    await session.commit()
    # Обновление статистики пользователя
    await update_user_stat(user_id, "delete", file.size)
    return True
