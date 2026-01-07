from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os
from routers import users_router, posts_router, roles_router


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
    allow_origins=["*"], # allow all for simplicity in this project
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users_router)
app.include_router(posts_router)
app.include_router(roles_router)


# serve static files from the react app
if os.path.exists("frontend/dist"):
    # mount assets separately for performance
    app.mount("/assets", StaticFiles(directory="frontend/dist/assets"), name="static")

    @app.get("/{full_path:path}")
    async def serve_frontend(full_path: str):
        # excluded paths (already handled by routers)
        if full_path.split('/')[0] in ["users", "posts", "roles", "docs", "openapi.json"]:
            raise HTTPException(status_code=404)
        
        return FileResponse("frontend/dist/index.html")
else:
    @app.get("/")
    def read_root():
        return {"status": "api is running, but frontend is not built. please run 'npm run build' in the frontend directory."}
