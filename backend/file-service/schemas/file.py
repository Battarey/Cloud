from pydantic import BaseModel, UUID4
from datetime import datetime

class FileCreate(BaseModel):
    filename: str
    size: int
    content_type: str

class FileRead(BaseModel):
    id: UUID4
    user_id: UUID4
    filename: str
    size: int
    content_type: str
    created_at: datetime
