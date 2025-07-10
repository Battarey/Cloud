from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class FileFilterParams(BaseModel):
    name: Optional[str] = Field(None, description="Фильтр по имени файла/папки (частичное совпадение)")
    created_from: Optional[datetime] = Field(None, description="Фильтр: дата создания от")
    created_to: Optional[datetime] = Field(None, description="Фильтр: дата создания до")
    size_min: Optional[int] = Field(None, description="Минимальный размер файла (байт)")
    size_max: Optional[int] = Field(None, description="Максимальный размер файла (байт)")
    file_type: Optional[str] = Field(None, description="Тип файла (например, 'image/png', 'folder', 'txt' и т.д.)")
