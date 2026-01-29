from pydantic import BaseModel, HttpUrl
from datetime import datetime

class URLCreate(BaseModel):
    long_url: HttpUrl

class URLResponse(BaseModel):
    short_code: str
    long_url: HttpUrl
    created_at: datetime

    class Config:
        orm_mode = True