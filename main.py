from fastapi import FastAPI, HTTPException
from typing import Optional, List, Dict
from pydantic import BaseModel
app = FastAPI()



class Post(BaseModel):
    id: int
    title: str
    body: str


posts = [
    {'id': 1, 'title': 'news_1', 'body': 'text_1'},
    {'id': 2, 'title': 'news_2', 'body': 'text_2'},
    {'id': 3, 'title': 'news_3', 'body': 'text_3'}
]

@app.get("/items")
async def items() -> List[Post]:
    post_list = []
    for post in posts:
        post_list.append(Post(id=post['id'], title=post['title'], body=post['body']))
    return post_list

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