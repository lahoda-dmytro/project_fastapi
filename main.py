from fastapi import FastAPI, HTTPException, Depends
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import delete
from models import base, User, Post, Role
from database import engine, async_session
from schemas import UserCreate, User as DbUser, PostCreate, Post as DbPost, Role as RoleSchema, RoleBase
from sqlalchemy.orm import selectinload

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# async def init_models():
#     async with engine.begin() as conn:
#         await conn.run_sync(base.metadata.create_all)

async def get_db():
    async with async_session() as session:
        yield session


@app.get("/")
def read_root():
    return {"main page"}



"""             roles           """

@app.post("/roles/", response_model=RoleSchema)
async def create_role(role: RoleBase, db: AsyncSession = Depends(get_db)):
    db_role = Role(name=role.name)
    db.add(db_role)
    await db.commit()
    await db.refresh(db_role)
    return db_role


@app.get("/roles/", response_model=List[RoleSchema])
async def get_roles(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Role))
    return result.scalars().all()



"""          users         """

@app.post("/users/", response_model=DbUser)
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


@app.get("/users/", response_model=List[DbUser])
async def get_users(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(User).options(selectinload(User.roles))
    )
    return result.scalars().all()


@app.get("/users/{user_id}", response_model=DbUser)
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(User).options(selectinload(User.roles)).where(User.id == user_id)
    )
    user = result.scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=404, detail="user not found")
    return user


@app.delete("/users/{user_id}", response_model=DbUser)
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


@app.put("/users/{user_id}", response_model=DbUser)
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



"""             posts           """

@app.post("/posts/", response_model=DbPost)
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


@app.get("/posts/", response_model=List[DbPost])
async def get_posts(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Post))
    return result.scalars().all()


@app.get("/posts/{post_id}", response_model=DbPost)
async def get_post(post_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Post).where(Post.id == post_id))
    post = result.scalar_one_or_none()
    if post is None:
        raise HTTPException(status_code=404, detail="post not found")
    return post


@app.delete("/posts/{post_id}", response_model=DbPost)
async def delete_post(post_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Post).where(Post.id == post_id))
    post = result.scalar_one_or_none()
    if post is None:
        raise HTTPException(status_code=404, detail="post not found")
    await db.delete(post)
    await db.commit()
    return post


@app.put("/posts/{post_id}", response_model=DbPost)
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
