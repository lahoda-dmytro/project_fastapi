from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from models import Role
from database import async_session
from schemas import Role as RoleSchema, RoleBase
from sqlalchemy.future import select
from typing import List
from database import get_db

router = APIRouter(prefix="/roles", tags=["roles"])


@router.post("/", response_model=RoleSchema)
async def create_role(role: RoleBase, db: AsyncSession = Depends(get_db)):
    db_role = Role(name=role.name)
    db.add(db_role)
    await db.commit()
    await db.refresh(db_role)
    return db_role


@router.get("/", response_model=List[RoleSchema])
async def get_roles(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Role))
    return result.scalars().all()
