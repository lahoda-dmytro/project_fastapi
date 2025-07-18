import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

load_dotenv()

SQL_DB_URL = os.getenv("DATABASE_URL")

engine = create_async_engine(SQL_DB_URL, echo=True)
async_session = sessionmaker(bind=engine, expire_on_commit=False, class_=AsyncSession)
base = declarative_base()
