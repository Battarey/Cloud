from pydantic import BaseModel, EmailStr, Field, field_validator
from uuid import UUID
import re

class UserCreate(BaseModel):
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=32, pattern=r'^[a-zA-Z0-9_]+$')
    password: str = Field(..., min_length=8, max_length=128)

    @field_validator('password')
    @classmethod
    def password_complexity(cls, v):
        if not re.search(r'[A-Z]', v):
            raise ValueError('Пароль должен содержать хотя бы одну заглавную букву')
        if not re.search(r'[a-z]', v):
            raise ValueError('Пароль должен содержать хотя бы одну строчную букву')
        if not re.search(r'[0-9]', v):
            raise ValueError('Пароль должен содержать хотя бы одну цифру')
        if not re.search(r'[^A-Za-z0-9]', v):
            raise ValueError('Пароль должен содержать хотя бы один спецсимвол')
        return v

class UserRead(BaseModel):
    id: UUID
    email: EmailStr
    username: str
    is_active: bool
    files_count: int
    files_size: int
    free_space: int

    class Config:
        orm_mode = True
