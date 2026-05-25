import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from fastapi import Depends

# Import your local config as a fallback
from app.core.config import DATABASE_URL as LOCAL_DB_URL

# 1. Grab the URL from Render. If it doesn't exist, fall back to your local config.
DATABASE_URL = os.getenv("DATABASE_URL", LOCAL_DB_URL)

if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL is not set")

# 2. Render gives 'postgres://' but modern SQLAlchemy strictly requires 'postgresql://'
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# 3. Create the engine and sessionmaker (duplicates removed)
engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()