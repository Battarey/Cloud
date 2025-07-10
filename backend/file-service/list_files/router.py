
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_async_session
from security.jwt import get_current_user
from .service import list_user_files
from schemas.file import FileRead
from typing import List, Optional

from filtration.schemas import FileFilterParams
from filtration.service import filter_files

router = APIRouter(prefix="/files", tags=["files"])

@router.get("/", response_model=List[FileRead])
async def list_files(
    folder_id: Optional[str] = None,
    name: Optional[str] = Query(None),
    created_from: Optional[str] = Query(None),
    created_to: Optional[str] = Query(None),
    size_min: Optional[int] = Query(None),
    size_max: Optional[int] = Query(None),
    file_type: Optional[str] = Query(None),
    user_id: str = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session)
):
    files = await list_user_files(user_id, folder_id, session)
    params = FileFilterParams(
        name=name,
        created_from=created_from,
        created_to=created_to,
        size_min=size_min,
        size_max=size_max,
        file_type=file_type
    )
    return filter_files(files, params)
