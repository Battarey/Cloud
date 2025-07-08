from sqlalchemy.ext.asyncio import AsyncSession
from models.file import File as FileModel
from sqlalchemy.future import select
from typing import List

async def list_user_files(user_id: str, folder_id: str | None, session: AsyncSession) -> List[FileModel]:
    query = select(FileModel).where(FileModel.user_id == user_id)
    if folder_id:
        query = query.where(FileModel.storage_key.startswith(f"{user_id}/{folder_id}/"))
    return (await session.execute(query)).scalars().all()
