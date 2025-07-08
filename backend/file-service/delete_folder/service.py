from sqlalchemy.ext.asyncio import AsyncSession
from models.file import File as FileModel
from storage.minio_client import minio_client, MINIO_BUCKET
from sqlalchemy.future import select

async def delete_folder_by_id(folder_id: str, user_id: str, session: AsyncSession):
    # Найти папку
    result = await session.execute(select(FileModel).where(FileModel.id == folder_id, FileModel.user_id == user_id, FileModel.content_type == 'folder'))
    folder = result.scalar_one_or_none()
    if not folder:
        return False
    # Найти все файлы внутри папки (по storage_key)
    prefix = folder.storage_key
    files_result = await session.execute(select(FileModel).where(FileModel.user_id == user_id, FileModel.storage_key.startswith(prefix)))
    files = files_result.scalars().all()
    # Удалить из MinIO и БД
    for file in files:
        minio_client.remove_object(MINIO_BUCKET, file.storage_key)
        await session.delete(file)
    await session.delete(folder)
    await session.commit()
    return True
