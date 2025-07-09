from sqlalchemy.ext.asyncio import AsyncSession
from models.file import File as FileModel
from minio_utils.minio_client import minio_client, MINIO_BUCKET
from sqlalchemy.future import select
from fastapi import HTTPException

async def get_file_for_download(file_id: str, user_id: str, session: AsyncSession):
    result = await session.execute(select(FileModel).where(FileModel.id == file_id, FileModel.user_id == user_id))
    file = result.scalar_one_or_none()
    if not file:
        raise HTTPException(status_code=404, detail="File not found")
    response = minio_client.get_object(MINIO_BUCKET, file.storage_key)
    return response, file
