# app/schemas.py
from typing import Optional
from sqlmodel import SQLModel


class UserBase(SQLModel):
    name: str
    email: str
    age: Optional[int] = None


class UserCreate(UserBase):
    pass


class UserRead(UserBase):
    id: int

    class Config:
        orm_mode = True


class UserUpdate(SQLModel):
    name: Optional[str] = None
    email: Optional[str] = None
    age: Optional[int] = None
