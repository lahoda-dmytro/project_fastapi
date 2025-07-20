from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from models import Role
from database import async_session
from schemas import Role as RoleSchema, RoleBase
from sqlalchemy.future import select
from typing import List

router = APIRouter(prefix="/roles", tags=["roles"])


async def get_db():
    async with async_session() as session:
        yield session


@router.post("/roles/", response_model=RoleSchema)
async def create_role(role: RoleBase, db: AsyncSession = Depends(get_db)):
    db_role = Role(name=role.name)
    db.add(db_role)
    await db.commit()
    await db.refresh(db_role)
    return db_role


@router.get("/roles/", response_model=List[RoleSchema])
async def get_roles(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Role))
    return result.scalars().all()
