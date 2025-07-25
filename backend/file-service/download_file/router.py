from fastapi import APIRouter, Depends, Response, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_async_session
from security.jwt import get_current_user
from .service import get_file_for_download

router = APIRouter(prefix="/files", tags=["files"])

@router.get("/{file_id}", description="Скачивание файла пользователем")
async def download_file(file_id: str, user_id: str = Depends(get_current_user), session: AsyncSession = Depends(get_async_session)):
    try:
        response, file = await get_file_for_download(file_id, user_id, session)
    except HTTPException as e:
        raise e
    return Response(content=response.read(), media_type=file.content_type, headers={"Content-Disposition": f"attachment; filename={file.filename}"})
