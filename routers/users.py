from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from models import User, Role, Post
from database import async_session
from schemas import UserCreate, User as DbUser
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from typing import List
from sqlalchemy import delete

router = APIRouter(prefix="/users", tags=["users"])


async def get_db():
    async with async_session() as session:
        yield session


@router.post("/users/", response_model=DbUser)
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_db)) -> DbUser:
    db_user = User(username=user.username, age=user.age)
    if user.roles:
        result = await db.execute(select(Role).where(Role.id.in_(user.roles)))
        db_user.roles = result.scalars().all()
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    result = await db.execute(
        select(User).options(selectinload(User.roles)).where(User.id == db_user.id)
    )
    db_user = result.scalar_one()
    return db_user


@router.get("/users/", response_model=List[DbUser])
async def get_users(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(User).options(selectinload(User.roles))
    )
    return result.scalars().all()


@router.get("/users/{user_id}", response_model=DbUser)
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(User).options(selectinload(User.roles)).where(User.id == user_id)
    )
    user = result.scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=404, detail="user not found")
    return user


@router.delete("/users/{user_id}", response_model=DbUser)
async def delete_user(user_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(User).options(selectinload(User.roles)).where(User.id == user_id)
    )
    user = result.scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=404, detail="user not found")
    await db.execute(delete(Post).where(Post.author_id == user.id))
    await db.delete(user)
    await db.commit()
    return user


@router.put("/users/{user_id}", response_model=DbUser)
async def update_user(user_id: int, user: UserCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(User).options(selectinload(User.roles)).where(User.id == user_id)
    )
    db_user = result.scalar_one_or_none()
    if db_user is None:
        raise HTTPException(status_code=404, detail="user not found")
    db_user.username = user.username
    db_user.age = user.age
    if user.roles:
        result = await db.execute(select(Role).where(Role.id.in_(user.roles)))
        db_user.roles = result.scalars().all()
    else:
        db_user.roles = []
    await db.commit()
    await db.refresh(db_user)
    return db_user
