from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,declarative_base, Session
from fastapi import Depends

DB_USER = "postgres"
DB_PASSWORD  = "vertin1999"
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "url_shortener"

DATABASE_URL = (
    f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

engine =  create_engine(DATABASE_URL)

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