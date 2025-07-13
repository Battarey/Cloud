from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_async_session
from security.jwt import get_current_user
from .service import delete_folder_by_id

router = APIRouter(prefix="/folders", tags=["folders"])

@router.delete("/{folder_id}")
async def delete_folder(folder_id: str, user_id: str = Depends(get_current_user), session: AsyncSession = Depends(get_async_session)):
    try:
        success = await delete_folder_by_id(folder_id, user_id, session)
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))
    if not success:
        raise HTTPException(status_code=404, detail="Folder not found")
    return {"status": "deleted"}
