from pydantic import BaseModel, HttpUrl
from datetime import datetime
from typing import Optional

class URLCreate(BaseModel):
    long_url: HttpUrl
    expires_at: Optional[datetime] = None

class URLResponse(BaseModel):
    short_code: str
    long_url: HttpUrl
    created_at: datetime
    expires_at: Optional[datetime]

    
class URLstats(BaseModel):
    short_code: str
    long_url: HttpUrl 
    access_count: int
    created_at: datetime
    expires_at: Optional[datetime]

    class Config:
        orm_mode = True
