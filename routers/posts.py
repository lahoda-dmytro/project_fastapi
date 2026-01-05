from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from schemas import PostCreate, Post as DbPost
from typing import List
from database import get_db
import crud

router = APIRouter(prefix="/posts", tags=["posts"])


@router.post("/", response_model=DbPost)
async def create_post(post: PostCreate, db: AsyncSession = Depends(get_db)) -> DbPost:
    db_post = await crud.create_post(db, post)
    if db_post is None:
        raise HTTPException(status_code=404, detail="user not found")
    return db_post


@router.get("/", response_model=List[DbPost])
async def get_posts(db: AsyncSession = Depends(get_db)):
    return await crud.get_posts(db)


@router.get("/{post_id}", response_model=DbPost)
async def get_post(post_id: int, db: AsyncSession = Depends(get_db)):
    post = await crud.get_post(db, post_id)
    if post is None:
        raise HTTPException(status_code=404, detail="post not found")
    return post


@router.delete("/{post_id}", response_model=DbPost)
async def delete_post(post_id: int, db: AsyncSession = Depends(get_db)):
    post = await crud.delete_post(db, post_id)
    if post is None:
        raise HTTPException(status_code=404, detail="post not found")
    return post


@router.put("/{post_id}", response_model=DbPost)
async def update_post(post_id: int, post: PostCreate, db: AsyncSession = Depends(get_db)):
    db_post = await crud.update_post(db, post_id, post)
    if db_post is None:
        raise HTTPException(status_code=404, detail="post not found")
    return db_post
