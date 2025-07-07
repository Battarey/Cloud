from fastapi import APIRouter
from pydantic import BaseModel
from .service import logout_user_service

class RefreshRequest(BaseModel):
    refresh_token: str

router = APIRouter(prefix="/logout", tags=["logout"])

@router.post("/")
async def logout(data: RefreshRequest):
    return await logout_user_service(data.refresh_token)
