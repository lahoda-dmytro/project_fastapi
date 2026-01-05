from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os
from routers import users_router, posts_router, roles_router

from contextlib import asynccontextmanager
from database import engine
from models import Base

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(
    title="fastapi project api",
    description="""
    this is a simple api for managing posts, users and roles.
    
    ## features
    * **users**: create, update, and manage users.
    * **posts**: create and delete posts by users.
    * **roles**: manage user permissions through roles.
    """,
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users_router)
app.include_router(posts_router)
app.include_router(roles_router)


# serve static files from the react app
if os.path.exists("frontend/dist"):
    app.mount("/assets", StaticFiles(directory="frontend/dist/assets"), name="static")

    @app.get("/{full_path:path}")
    async def serve_frontend(full_path: str):
        # check if requested path is an api route
        if full_path.startswith("api/") or full_path.startswith("users") or full_path.startswith("posts") or full_path.startswith("roles"):
            return None # let fastapi handle it normally
        
        # serve index.html for all other routes to support react router
        return FileResponse("frontend/dist/index.html")
else:
    @app.get("/")
    def read_root():
        return {"status": "api is running, but frontend is not built"}
