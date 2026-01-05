from pydantic import BaseModel, Field
from datetime import datetime
from .role import Role


class UserBase(BaseModel):
    username: str
    age: int = Field(..., ge=0, le=100)

    class Config:
        from_attributes = True
        json_schema_extra  = {
            "example": {
                "id": 1,
                "username": "entomb3nt",
                "age": 20,
                "roles": [
                    {
                        "id": 2,
                        "name": "admin"
                    }
                ]
            }
        }


class UserCreate(UserBase):
    password: str
    roles: list[int]

    class Config:
        json_schema_extra  = {
            "example": {
                "username": "yung lean",
                "age": 28,
                "roles": [1, 3]
            }
        }

class User(UserBase):
    id: int
    roles: list[Role]
    created_at: datetime

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "username": "entomb3nt",
                "age": 20,
                "roles": [
                    {
                        "id": 2,
                        "name": "admin"
                    },
                    {
                        "id": 3,
                        "name": "user"
                    }
                ]
            }
        }
