from fastapi import FastAPI, HTTPException, Depends
from typing import  List
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware

from models import base, User, Post, Role
from database import engine, session_local
from schemas import UserCreate, User as DbUser, PostCreate, Post as DbPost, Role as RoleSchema, RoleBase
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

base.metadata.create_all(bind=engine)

def get_db():
    db = session_local()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"main page"}

@app.post("/roles/", response_model=RoleSchema)
def create_role(role: RoleBase, db: Session = Depends(get_db)):
    db_role = Role(name=role.name)
    db.add(db_role)
    db.commit()
    db.refresh(db_role)
    return db_role

@app.get("/roles/", response_model=List[RoleSchema])
def get_roles(db: Session = Depends(get_db)):
    return db.query(Role).all()

@app.post("/users/", response_model=DbUser)
async def create_user(user: UserCreate, db: Session = Depends(get_db)) -> DbUser:
    db_user = User(username=user.username, age=user.age)   #hashed_password="test"hashed_password="test"hashed_password="test"
    if user.roles:
        db_user.roles = db.query(Role).filter(Role.id.in_(user.roles)).all()
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.post("/posts/", response_model=DbPost)
async def create_post(post: PostCreate, db: Session = Depends(get_db)) -> DbPost:
    db_user = db.query(User).filter(User.id == post.author_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="user not found")

    db_post = Post(title= post.title, body=post.body, author_id=post.author_id)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)

    return db_post


@app.get("/posts/", response_model=List[DbPost])
async def get_posts(db: Session = Depends(get_db)):
    return db.query(Post).all()


@app.delete("/posts/{post_id}", response_model=DbPost)
async def delete_post(post_id: int, db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.id == post_id).first()
    if post is None:
        raise HTTPException(status_code=404, detail="post not found")
    db.delete(post)
    db.commit()
    return post


@app.put("/posts/{post_id}", response_model=DbPost)
async def update_post(post_id: int, post: PostCreate, db: Session = Depends(get_db)):
    db_post = db.query(Post).filter(Post.id == post_id).first()
    if db_post is None:
        raise HTTPException(status_code=404, detail="post not found")
    db_post.title = post.title
    db_post.body = post.body
    db_post.author_id = post.author_id
    db.commit()
    db.refresh(db_post)
    return db_post

@app.get("/posts/{post_id}", response_model=DbPost)
async def get_post(post_id: int, db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.id == post_id).first()
    if post is None:
        raise HTTPException(status_code=404, detail="post not found")
    return post


@app.get("/users/", response_model=List[DbUser])
async def get_users(db: Session = Depends(get_db)):
    return db.query(User).all()

@app.get("/users/{user_id}", response_model=DbUser)
async def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="user not found")
    return user


@app.delete("/users/{user_id}", response_model=DbUser)
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="user not found")
    db.delete(user)
    db.commit()
    return user


@app.put("/users/{user_id}", response_model=DbUser)
async def update_user(user_id: int, user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="user not found")
    db_user.username = user.username
    db_user.age = user.age
    if user.roles:
        db_user.roles = db.query(Role).filter(Role.id.in_(user.roles)).all()
    else:
        db_user.roles = []
    db.commit()
    db.refresh(db_user)
    return db_user
