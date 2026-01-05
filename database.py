import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

SQL_DB_URL = "sqlite+aiosqlite:///./test.db"

engine = create_async_engine(SQL_DB_URL, echo=True)
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

async def get_db():
    async with async_session() as db:
        yield db