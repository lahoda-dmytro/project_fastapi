from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from models import Role
from schemas import Role as RoleSchema, RoleBase
from sqlalchemy.future import select
from typing import List
from database import get_db

router = APIRouter(prefix="/roles", tags=["roles"])


@router.post("/", response_model=RoleSchema, summary="create a new role")
async def create_role(role: RoleBase, db: AsyncSession = Depends(get_db)):
    """
    create a new permission role.
    """
    db_role = Role(name=role.name)
    db.add(db_role)
    await db.commit()
    await db.refresh(db_role)
    return db_role


@router.get("/", response_model=List[RoleSchema], summary="get all roles")
async def get_roles(db: AsyncSession = Depends(get_db)):
    """
    retrieve a list of all available roles.
    """
    result = await db.execute(select(Role))
    return result.scalars().all()
