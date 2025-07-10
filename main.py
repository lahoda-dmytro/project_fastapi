from fastapi import FastAPI, HTTPException, Path, Query, Depends
from typing import Optional, List, Dict, Annotated
from sqlalchemy.orm import Session


from models import base, User, Post
from database import engine, session_local
from schemas import UserCreate, User as DbUser, PostCreate, Post as DbPost

app = FastAPI()

base.metadata.create_all(bind=engine)

def get_db():
    db = session_local()
    try:
        yield db
    finally:
        db.close()


@app.post("/users/", response_model=DbUser)
async def create_user(user: UserCreate, db: Session = Depends(get_db)) -> DbUser:
    db_user = User(username=user.username, age= user.age)
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
    return db.query(DbPost).all()



# @app.get("/items")
# async def items() -> List[Post]:
#     return [Post(**post) for post in posts]
#
# @app.post("/items/add")
# async def add_item(post: PostCreate) -> Post:
#     author = next((user for user in users if user['id'] == post.author_id), None)
#     if not author:
#         raise HTTPException(status_code=404, detail="user not found")
#
#     new_post_id = max((p['id'] for p in posts), default=0) + 1
#
#     new_post = {'id': new_post_id,
#         'title': post.title,
#         'body': post.body,
#         'author': author}
#
#     posts.append(new_post)
#
#     return Post(**new_post)
#
# @app.post("/user/add")
# async def user_add(user: UserCreate) -> User:
#     new_user_id = max((user_id['id'] for user_id in users), default=0) + 1
#     new_user = {'id': new_user_id,
#         'username': user.username,
#         'age': user.age }
#
#     posts.append(new_user)
#
#     return User(**new_user)
#
# @app.delete("/items/delete/{id}")
# async def delete_item(id: Annotated[int, Path(..., title="post`s id", ge=1)]) -> Post:
#    for index, post in enumerate(posts):
#        if post['id'] == id:
#            deleted_post = posts.pop(index)
#            return Post(**deleted_post)
#    raise HTTPException(status_code=404, detail="item not found")
#
# @app.get("/items/{id}")
# async def items(id: Annotated[int, Path(title='post`s id', ge=1)]) -> Post:
#     for i in posts:
#         if i['id'] == id:
#             return Post(**i)
#     raise HTTPException(status_code=404, detail="post not found")
#
# @app.get("/search")
# async def search(post_id: Annotated[Optional[int], Query(title="id of post to search", ge=1 ,le=50)])\
#         -> Dict[str, Optional[Post]]:
#     if post_id:
#         for i in posts:
#             if i['id'] == post_id:
#                 return {"data": Post(**i)}
#         raise HTTPException(status_code=404, detail="post not found")
#     else:
#         return {"data": None}
#
