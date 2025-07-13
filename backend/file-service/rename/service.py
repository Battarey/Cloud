from sqlalchemy.ext.asyncio import AsyncSession
from models.file import File as FileModel
from sqlalchemy.future import select
from fastapi import HTTPException
import uuid
import re

async def rename_file(file_id: str, user_id: str, new_name: str, session: AsyncSession):
    # Проверка UUID
    try:
        file_uuid = uuid.UUID(file_id)
    except (ValueError, TypeError):
        raise HTTPException(status_code=404, detail="File not found")
    # Проверка валидности имени
    if not new_name or len(new_name) > 255 or re.search(r'[\\/:*?"<>|]', new_name):
        raise HTTPException(status_code=400, detail="Invalid file name")
    # Проверка на дубликат
    dup_result = await session.execute(select(FileModel).where(FileModel.user_id == user_id, FileModel.filename == new_name, FileModel.id != file_uuid))
    duplicate = dup_result.scalar_one_or_none()
    if duplicate:
        raise HTTPException(status_code=409, detail="File with this name already exists")
    # Переименование
    result = await session.execute(select(FileModel).where(FileModel.id == file_uuid, FileModel.user_id == user_id))
    file = result.scalar_one_or_none()
    if not file:
        raise HTTPException(status_code=404, detail="File not found")
    file.filename = new_name
    await session.commit()
    await session.refresh(file)
    return file

async def rename_folder(folder_id: str, user_id: str, new_name: str, session: AsyncSession):
    # Проверка UUID
    try:
        folder_uuid = uuid.UUID(folder_id)
    except (ValueError, TypeError):
        raise HTTPException(status_code=404, detail="Folder not found")
    # Проверка валидности имени
    if not new_name or len(new_name) > 255 or re.search(r'[\\/:*?"<>|]', new_name):
        raise HTTPException(status_code=400, detail="Invalid folder name")
    # Проверка на дубликат
    dup_result = await session.execute(select(FileModel).where(
        FileModel.user_id == user_id,
        FileModel.filename == new_name,
        FileModel.content_type == 'folder',
        FileModel.id != folder_uuid
    ))
    duplicate = dup_result.scalar_one_or_none()
    if duplicate:
        raise HTTPException(status_code=409, detail="Folder with this name already exists")
    # Переименование
    result = await session.execute(select(FileModel).where(
        FileModel.id == folder_uuid,
        FileModel.user_id == user_id,
        FileModel.content_type == 'folder'))
    folder = result.scalar_one_or_none()
    if not folder:
        raise HTTPException(status_code=404, detail="Folder not found")
    folder.filename = new_name
    await session.commit()
    await session.refresh(folder)
    return folder
