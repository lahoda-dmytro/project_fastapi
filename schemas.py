from pydantic import BaseModel, Field


class UserBase(BaseModel):
    username: str
    age: int = Field(..., ge=0, le=100)

class UserCreate(UserBase):
    pass


class User(UserBase):
    id: int

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