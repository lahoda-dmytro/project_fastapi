from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from models import User, Post
from database import async_session
from schemas import PostCreate, Post as DbPost
from sqlalchemy.future import select
from typing import List
from database import get_db

router = APIRouter(prefix="/posts", tags=["posts"])


@router.post("/", response_model=DbPost)
async def create_post(post: PostCreate, db: AsyncSession = Depends(get_db)) -> DbPost:
    result = await db.execute(select(User).where(User.id == post.author_id))
    db_user = result.scalar_one_or_none()
    if db_user is None:
        raise HTTPException(status_code=404, detail="user not found")
    db_post = Post(title=post.title, body=post.body, author_id=post.author_id)
    db.add(db_post)
    await db.commit()
    await db.refresh(db_post)
    return db_post


@router.get("/", response_model=List[DbPost])
async def get_posts(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Post))
    return result.scalars().all()


@router.get("/{post_id}", response_model=DbPost)
async def get_post(post_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Post).where(Post.id == post_id))
    post = result.scalar_one_or_none()
    if post is None:
        raise HTTPException(status_code=404, detail="post not found")
    return post


@router.delete("/{post_id}", response_model=DbPost)
async def delete_post(post_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Post).where(Post.id == post_id))
    post = result.scalar_one_or_none()
    if post is None:
        raise HTTPException(status_code=404, detail="post not found")
    await db.delete(post)
    await db.commit()
    return post


@router.put("/{post_id}", response_model=DbPost)
async def update_post(post_id: int, post: PostCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Post).where(Post.id == post_id))
    db_post = result.scalar_one_or_none()
    if db_post is None:
        raise HTTPException(status_code=404, detail="post not found")
    db_post.title = post.title
    db_post.body = post.body
    db_post.author_id = post.author_id
    await db.commit()
    await db.refresh(db_post)
    return db_post
