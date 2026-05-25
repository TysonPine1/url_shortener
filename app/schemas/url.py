from pydantic import BaseModel, HttpUrl, ConfigDict
from datetime import datetime
from typing import Optional

class URLCreate(BaseModel):
    long_url: HttpUrl
    expires_at: Optional[datetime] = None

    # @field_validator("expires_at")
    # def force_utc(cls, v):
    #     if v is not None and v.tzinfo is None:
    #         raise ValueError("expires_at must be timezone-aware")
    #     return v

class URLResponse(BaseModel):
    short_code: str
    long_url: HttpUrl
    created_at: datetime
    expires_at: datetime

    model_config = ConfigDict(from_attributes=True)

class URLstats(BaseModel):
    short_code: str
    long_url: HttpUrl 
    access_count: int
    created_at: datetime
    expires_at: Optional[datetime]

    class Config:
        from_attributes = True

