from pydantic import BaseModel


class RoleBase(BaseModel):
    name: str

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "name": "admin",
                "id": 1
              }
        }

class Role(RoleBase):
    id: int

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "name": "admin",
                "id": 1
            }
        }

