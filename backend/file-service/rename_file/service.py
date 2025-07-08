from sqlalchemy.ext.asyncio import AsyncSession
from models.file import File as FileModel
from sqlalchemy.future import select
from fastapi import HTTPException

async def rename_file(file_id: str, user_id: str, new_name: str, session: AsyncSession):
    result = await session.execute(select(FileModel).where(FileModel.id == file_id, FileModel.user_id == user_id))
    file = result.scalar_one_or_none()
    if not file:
        raise HTTPException(status_code=404, detail="File not found")
    file.filename = new_name
    await session.commit()
    await session.refresh(file)
    return file
