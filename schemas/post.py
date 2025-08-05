from pydantic import BaseModel


class PostBase(BaseModel):
    title: str
    body: str
    author_id: int

    class Config:
        json_schema_extra = {
            "example": {
                "title": "7.39c Gameplay Patch",
                "body": "Patch 7.39c is out now and you can check out the patch notes here.",
                "author_id": 1
            }
        }

class PostCreate(PostBase):
    pass


class Post(PostBase):
    id: int

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "title": "7.39c Gameplay Patch",
                "body": "Patch 7.39c is out now and you can check out the patch notes here.",
                "author_id": 1,
                "id": 32
            }
        }
