import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

SQL_DB_URL = os.getenv("DATABASE_URL")

engine = create_engine(SQL_DB_URL, connect_args={"check_same_thread": False} if "sqlite" in SQL_DB_URL else {})

session_local = sessionmaker(autoflush=False, autocommit=False, bind=engine)

base = declarative_base()