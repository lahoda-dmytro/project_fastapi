from pydantic import BaseModel, Field
from typing import List
from .role import Role


class UserBase(BaseModel):
    username: str
    age: int = Field(..., ge=0, le=100)


class UserCreate(UserBase):
    roles: List[int] = []


class User(UserBase):
    id: int
    roles: List[Role] = []

    class Config:
        from_attributes = True
