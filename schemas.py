from pydantic import BaseModel

class UserBase(BaseModel):
    username: str
    age: int

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