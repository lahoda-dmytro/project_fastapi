from fastapi import FastAPI, HTTPException, Path, Query
from typing import Optional, List, Dict, Annotated
from pydantic import BaseModel, Field
app = FastAPI()


class User(BaseModel):
    id: int
    username: str
    age: int


class Post(BaseModel):
    id: int
    title: str
    body: str
    author: User


class PostCreate(BaseModel):
    title: str
    body: str
    author_id: int


class UserCreate(BaseModel):
    username: Annotated[str, Field(..., title="user`s name")]
    age: Annotated[int, Field(..., title="user`s age")]


users = [
    {'id': 1, 'username': 'user1', 'age': 1},
    {'id': 2, 'username': 'user2', 'age': 2},
    {'id': 3, 'username': 'user3', 'age': 3},
]

posts = [
    {'id': 1, 'title': 'news_1', 'body': 'text_1', 'author': users[0]},
    {'id': 2, 'title': 'news_2', 'body': 'text_2', 'author': users[1]},
    {'id': 3, 'title': 'news_3', 'body': 'text_3', 'author': users[2]},
]

@app.get("/items")
async def items() -> List[Post]:
    return [Post(**post) for post in posts]

@app.post("/items/add")
async def add_item(post: PostCreate) -> Post:
    author = next((user for user in users if user['id'] == post.author_id), None)
    if not author:
        raise HTTPException(status_code=404, detail="user not found")

    new_post_id = max((p['id'] for p in posts), default=0) + 1

    new_post = {'id': new_post_id,
        'title': post.title,
        'body': post.body,
        'author': author}

    posts.append(new_post)

    return Post(**new_post)

@app.post("/user/add")
async def user_add(user: UserCreate) -> User:
    new_user_id = max((user_id['id'] for user_id in users), default=0) + 1
    new_user = {'id': new_user_id,
        'username': user.username,
        'age': user.age }

    posts.append(new_user)

    return User(**new_user)

@app.delete("/items/delete/{id}")
async def delete_item(id: Annotated[int, Path(..., title="post`s id", ge=1)]) -> Post:
   for index, post in enumerate(posts):
       if post['id'] == id:
           deleted_post = posts.pop(index)
           return Post(**deleted_post)
   raise HTTPException(status_code=404, detail="item not found")

@app.get("/items/{id}")
async def items(id: Annotated[int, Path(title='post`s id', ge=1)]) -> Post:
    for i in posts:
        if i['id'] == id:
            return Post(**i)
    raise HTTPException(status_code=404, detail="post not found")

@app.get("/search")
async def search(post_id: Annotated[Optional[int], Query(title="id of post to search", ge=1 ,le=50)])\
        -> Dict[str, Optional[Post]]:
    if post_id:
        for i in posts:
            if i['id'] == post_id:
                return {"data": Post(**i)}
        raise HTTPException(status_code=404, detail="post not found")
    else:
        return {"data": None}

