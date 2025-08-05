from pydantic import BaseModel, Field
from .role import Role


class UserBase(BaseModel):
    username: str
    age: int = Field(..., ge=0, le=100)


class UserCreate(UserBase):
    roles: list[int]


class User(UserBase):
    id: int
    roles: list[Role]

    class Config:
        from_attributes = True
