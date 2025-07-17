from pydantic import BaseModel, Field
from typing import List


class UserBase(BaseModel):
    username: str
    age: int = Field(..., ge=0, le=100)

class UserCreate(UserBase):
    roles: List[int] = []



class RoleBase(BaseModel):
    name: str

class Role(RoleBase):
    id: int
    class Config:
        from_attributes = True

class User(UserBase):
    id: int
    roles: List[Role] = []
    class Config:
        from_attributes = True


class PostBase(BaseModel):
    title: str
    body: str
    author_id: int


class PostCreate(PostBase):
    pass


class Post(PostBase):
    id: int

    class Config:
        from_attributes = True
