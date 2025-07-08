from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_async_session
from security.jwt import get_current_user
from .service import create_folder

router = APIRouter(prefix="/folders", tags=["folders"])

@router.post("/create")
async def create_folder_endpoint(folder_name: str, user_id: str = Depends(get_current_user), session: AsyncSession = Depends(get_async_session)):
    folder = await create_folder(user_id, folder_name, session)
    return {"id": folder.id, "name": folder.filename, "status": "created"}
