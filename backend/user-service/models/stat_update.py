from pydantic import BaseModel
from uuid import UUID

class StatUpdate(BaseModel):
    user_id: UUID
    file_size: int  # размер файла в байтах
    action: str  # 'upload' или 'delete'
