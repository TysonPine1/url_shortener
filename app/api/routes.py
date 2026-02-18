from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import RedirectResponse    
from sqlalchemy.orm import Session
from datetime import datetime, timezone, timedelta

from app.schemas.url import URLCreate, URLResponse, URLstats
from app.models.url import URL
from app.services.shortener import generate_short_code
from app.db.database import get_db
from app.services.shortener import generate_unique_short_code
print(datetime.utcnow())
router = APIRouter()

@router.post("/shorten", response_model=URLResponse, status_code=status.HTTP_201_CREATED)
def create_short_url(payload: URLCreate, db: Session = Depends(get_db)):

    now = datetime.utcnow()

    if payload.expires_at is None:
        expires_at = now + timedelta(minutes=5)
    else:
        expires_at =  payload.expires_at
        if expires_at.tzinfo is not None:
            expires_at = expires_at.replace(tzinfo=None)
        if expires_at < now:
            raise HTTPException(
                status_code=400,
                detail="Expire must be in the future"
            )
        
    # else:
    #     expires_at = payload.expires_at

        # if expires_at.tzinfo is None:
        #     expires_at = expires_at.replace(tzinfo=timezone.utc)

        # if expires_at < now:
        #     raise HTTPException(
        #         status_code=400,
        #         detail="Expire must be in the future"
        #     )

    short_code = generate_unique_short_code(db)

    url = URL(
        long_url=str(payload.long_url),
        short_code=short_code,
        access_count=0,
        expires_at=expires_at
    )

    db.add(url)
    db.commit()
    db.refresh(url)

    return url

@router.get("/{short_code}", status_code=status.HTTP_302_FOUND, include_in_schema=False)
def redirect_url(short_code: str, db: Session = Depends(get_db)):
    url = db.query(URL).filter(URL.short_code == short_code).first()

    if not url:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Short URL not found")

    if url.expires_at:
        expires_at = url.expires_at
        if expires_at.tzinfo is None:
            expires_at = expires_at.replace(tzinfo=timezone.utc)
        if expires_at < datetime.now(timezone.utc):
            raise HTTPException(status_code=status.HTTP_410_GONE, detail="Short URL has expired")
        if url.expires_at and url.expires_at < datetime.utcnow():
            raise HTTPException(
                status_code=status.HTTP_410_GONE,
                detail="Short URL has expired"
            )
    # if url.expires_at and url.expires_at < datetime.now(timezone.utc):
    #     raise HTTPException(status_code=status.HTTP_410_GONE, detail="Short URL has expired")

    url.access_count += 1
    db.commit()

    return RedirectResponse(url=url.long_url)

@router.get("/stats/{short_code}", response_model=URLstats)
def get_url_stats(short_code: str, db: Session = Depends(get_db)):
    url = db.query(URL).filter(URL.short_code == short_code).first()

    if not url:
        raise HTTPException(status_code=404, detail="Short URL not found")

    return url