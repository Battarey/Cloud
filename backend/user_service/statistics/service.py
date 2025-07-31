from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.user import User
from models.stat_update import StatUpdate
from fastapi import HTTPException

async def update_user_stat(data: StatUpdate, session: AsyncSession):
    result = await session.execute(select(User).where(User.id == data.user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if data.action == "upload":
        user.files_count += 1
        user.files_size += data.file_size
        user.free_space -= data.file_size
    elif data.action == "delete":
        user.files_count = max(user.files_count - 1, 0)
        user.files_size = max(user.files_size - data.file_size, 0)
        user.free_space += data.file_size
    else:
        raise HTTPException(status_code=400, detail="Invalid action")
    await session.commit()
    await session.refresh(user)
    return {"status": "ok", "files_count": user.files_count, "files_size": user.files_size, "free_space": user.free_space}
