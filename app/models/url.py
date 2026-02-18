from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime, timezone, timedelta

from app.db.database import Base

class URL(Base):
    __tablename__ = "urls"

    id = Column(Integer, primary_key=True, index=True)
    long_url = Column(String, nullable=False)
    short_code = Column(String, unique=True, index=True, nullable=False)

    access_count = Column(Integer, default=0)

    expires_at = Column(DateTime, default=lambda: datetime.utcnow() + timedelta(minutes=5))

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow,onupdate=datetime.utcnow) 