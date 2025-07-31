from pydantic import BaseModel
from uuid import UUID

from pydantic import field_validator

class StatUpdate(BaseModel):
    user_id: UUID
    file_size: int  # размер файла в байтах
    action: str  # 'upload' или 'delete'

    @field_validator('file_size')
    @classmethod
    def file_size_non_negative(cls, v):
        if v < 0:
            raise ValueError('file_size must be non-negative')
        return v
