from fastapi import FastAPI, HTTPException
from typing import Optional, List, Dict
from pydantic import BaseModel
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

@app.get("/item/{id}")
async def item(id: int) -> Post:
    for i in posts:
        if i['id'] == id:
            return Post(**i)
    raise HTTPException(status_code=404, detail="post not found")

@app.get("/search")
async def search(post_id: Optional[int] = None) -> Dict[str, Optional[Post]]:
    if post_id:
        for i in posts:
            if i['id'] == post_id:
                return {"data": Post(**i)}
        raise HTTPException(status_code=404, detail="post not found")
    else:
        return {"data": None}