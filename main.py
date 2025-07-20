from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import users_router, posts_router, roles_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users_router)
app.include_router(posts_router)
app.include_router(roles_router)


@app.get("/")
def read_root():
    return {"main page"}
