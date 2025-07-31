from sqlalchemy.ext.asyncio import AsyncSession
from models.user import User

async def delete_account_service(current_user: User, session: AsyncSession):
    await session.delete(current_user)
    await session.commit()
    return {"status": "deleted"}
