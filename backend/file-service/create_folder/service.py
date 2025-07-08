from sqlalchemy.ext.asyncio import AsyncSession
from models.file import File as FileModel
import uuid

async def create_folder(user_id: str, folder_name: str, session: AsyncSession):
    # Папка как файл с content_type = 'folder', size = 0
    folder_id = str(uuid.uuid4())
    db_folder = FileModel(
        id=folder_id,
        user_id=user_id,
        filename=folder_name,
        size=0,
        content_type='folder',
        storage_key=f"{user_id}/{folder_id}/{folder_name}/"
    )
    session.add(db_folder)
    await session.commit()
    await session.refresh(db_folder)
    return db_folder
