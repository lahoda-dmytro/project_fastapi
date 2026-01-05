from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from sqlalchemy import delete
from models import User, Role, Post
from schemas import UserCreate
import bcrypt

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

async def get_user(db: AsyncSession, user_id: int):
    result = await db.execute(
        select(User).options(selectinload(User.roles)).where(User.id == user_id)
    )
    return result.scalar_one_or_none()

async def get_users(db: AsyncSession):
    result = await db.execute(select(User).options(selectinload(User.roles)))
    return result.scalars().all()

async def create_user(db: AsyncSession, user: UserCreate):
    hashed_password = hash_password(user.password)
    db_user = User(username=user.username, age=user.age, hashed_password=hashed_password)
    if user.roles:
        result = await db.execute(select(Role).where(Role.id.in_(user.roles)))
        db_user.roles = result.scalars().all()
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    # Re-fetch to load relationships
    return await get_user(db, db_user.id)

async def delete_user(db: AsyncSession, user_id: int):
    user = await get_user(db, user_id)
    if user:
        await db.execute(delete(Post).where(Post.author_id == user.id))
        await db.delete(user)
        await db.commit()
    return user

async def update_user(db: AsyncSession, user_id: int, user_update: UserCreate):
    db_user = await get_user(db, user_id)
    if db_user:
        db_user.username = user_update.username
        db_user.age = user_update.age
        # Update password if needed, though usually update endpoint might separate this
        # For now, following existing pattern of updating all fields from input
        if user_update.password:
             db_user.hashed_password = hash_password(user_update.password)
        
        if user_update.roles:
            result = await db.execute(select(Role).where(Role.id.in_(user_update.roles)))
            db_user.roles = result.scalars().all()
        else:
            db_user.roles = []
            
        await db.commit()
        await db.refresh(db_user)
    return db_user
