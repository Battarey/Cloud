from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_async_session
from security.jwt import get_current_user
from .service import delete_file_by_id

router = APIRouter(prefix="/files", tags=["files"])

@router.delete("/{file_id}", description="Удаление файла пользователем")
async def delete_file(file_id: str, user_id: str = Depends(get_current_user), session: AsyncSession = Depends(get_async_session)):
    success = await delete_file_by_id(file_id, user_id, session)
    if not success:
        raise HTTPException(status_code=404, detail="File not found")
    return {"status": "deleted"}
