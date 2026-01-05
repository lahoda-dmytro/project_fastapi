from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models import Post, User
from schemas import PostCreate

async def get_post(db: AsyncSession, post_id: int):
    result = await db.execute(select(Post).where(Post.id == post_id))
    return result.scalar_one_or_none()

async def get_posts(db: AsyncSession):
    result = await db.execute(select(Post))
    return result.scalars().all()

async def create_post(db: AsyncSession, post: PostCreate):
    # Check if author exists
    result = await db.execute(select(User).where(User.id == post.author_id))
    if not result.scalar_one_or_none():
        return None
        
    db_post = Post(title=post.title, body=post.body, author_id=post.author_id)
    db.add(db_post)
    await db.commit()
    await db.refresh(db_post)
    return db_post

async def delete_post(db: AsyncSession, post_id: int):
    post = await get_post(db, post_id)
    if post:
        await db.delete(post)
        await db.commit()
    return post

async def update_post(db: AsyncSession, post_id: int, post_update: PostCreate):
    db_post = await get_post(db, post_id)
    if db_post:
        db_post.title = post_update.title
        db_post.body = post_update.body
        db_post.author_id = post_update.author_id
        await db.commit()
        await db.refresh(db_post)
    return db_post
