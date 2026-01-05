from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from schemas import PostCreate, Post as DbPost
from typing import List
from database import get_db
import crud

router = APIRouter(prefix="/posts", tags=["posts"])


@router.post("/", response_model=DbPost, summary="create a new post")
async def create_post(post: PostCreate, db: AsyncSession = Depends(get_db)) -> DbPost:
    """
    create a new blog post for a specific user.
    """
    db_post = await crud.create_post(db, post)
    if db_post is None:
        raise HTTPException(status_code=404, detail="user not found")
    return db_post


@router.get("/", response_model=List[DbPost], summary="get all posts")
async def get_posts(db: AsyncSession = Depends(get_db)):
    """
    retrieve a list of all posts in the system.
    """
    return await crud.get_posts(db)


@router.get("/{post_id}", response_model=DbPost, summary="get post by id")
async def get_post(post_id: int, db: AsyncSession = Depends(get_db)):
    """
    retrieve details for a specific post.
    """
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
