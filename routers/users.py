from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from schemas import UserCreate, User as DbUser
from typing import List
from database import get_db
import crud

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", response_model=DbUser)
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_db)) -> DbUser:
    return await crud.create_user(db, user)


@router.get("/", response_model=List[DbUser])
async def get_users(db: AsyncSession = Depends(get_db)):
    return await crud.get_users(db)


@router.get("/{user_id}", response_model=DbUser)
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
    user = await crud.get_user(db, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="user not found")
    return user


@router.delete("/{user_id}", response_model=DbUser)
async def delete_user(user_id: int, db: AsyncSession = Depends(get_db)):
    user = await crud.delete_user(db, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="user not found")
    return user


@router.put("/{user_id}", response_model=DbUser)
async def update_user(user_id: int, user: UserCreate, db: AsyncSession = Depends(get_db)):
    db_user = await crud.update_user(db, user_id, user)
    if db_user is None:
        raise HTTPException(status_code=404, detail="user not found")
    return db_user
