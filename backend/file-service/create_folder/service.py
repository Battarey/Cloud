from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models.file import File as FileModel
import uuid
import re

class FolderCreateError(Exception):
    def __init__(self, status_code: int, detail: str):
        self.status_code = status_code
        self.detail = detail

async def create_folder(user_id: str, folder_name: str, session: AsyncSession):
    # Проверка на пустое имя
    if not folder_name or folder_name.strip() == "":
        raise FolderCreateError(422, "Folder name cannot be empty")
    # Проверка на длину
    if len(folder_name) > 255:
        raise FolderCreateError(422, "Folder name too long")
    # Проверка на недопустимые символы (только буквы, цифры, подчёркивание, дефис, пробел)
    if not re.match(r'^[\w\- ]+$', folder_name):
        raise FolderCreateError(400, "Folder name contains invalid characters")

    # Проверка на дубликаты
    query = select(FileModel).where(
        FileModel.user_id == user_id,
        FileModel.filename == folder_name,
        FileModel.content_type == 'folder'
    )
    result = await session.execute(query)
    existing = result.scalar_one_or_none()
    if existing:
        raise FolderCreateError(409, "Folder already exists")

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
