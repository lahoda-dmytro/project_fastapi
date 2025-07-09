from fastapi import FastAPI, HTTPException
from typing import Optional
app = FastAPI()


# @app.get("/")
# async def root():
#     return {"message": "Hello World"}
#
#
# @app.get("/hello/{name}")
# async def say_hello(name: str):
#     return {"message": f"Hello {name}"}
#

posts = [
    {'id': 1, 'title': 'news_1', 'body': 'text_1'},
    {'id': 2, 'title': 'news_2', 'body': 'text_2'},
    {'id': 3, 'title': 'news_3', 'body': 'text_3'}
]

@app.get("/items")
async def items() -> list:
    return posts


@app.get("/item/{id}")
async def item(id: int) -> dict:
    for i in posts:
        if i['id'] == id:
            return i
    raise HTTPException(status_code=404, detail="post not found")

@app.get("/search")
async def search(post_id: Optional[int] = None) -> dict:
    if post_id:
        for i in posts:
            if i['id'] == post_id:
                return i
        raise HTTPException(status_code=404, detail="post not found")
    else:
        return {"message": "haven`t post id"}