from pydantic import BaseModel, UUID4, Field, field_validator
from datetime import datetime
import re

class FileCreate(BaseModel):
    filename: str = Field(..., min_length=1, max_length=255)
    size: int
    content_type: str

    @field_validator('filename')
    @classmethod
    def validate_filename(cls, v):
        if re.search(r'[\\/:*?"<>|]', v):
            raise ValueError("Недопустимые символы в названии файла")
        return v

class FileRead(BaseModel):
    id: UUID4
    user_id: UUID4
    filename: str
    size: int
    content_type: str
    created_at: datetime

class FolderCreate(BaseModel):
    folder_name: str = Field(..., min_length=1, max_length=260)
    parent_folder_id: UUID4 | None = None

    @field_validator('folder_name')
    @classmethod
    def validate_folder_name(cls, v):
        if re.search(r'[\\/:*?"<>|]', v):
            raise ValueError("Недопустимые символы в названии папки")
        return v
