from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import RedirectResponse    
from sqlalchemy.orm import Session
from datetime import datetime

from app.schemas.url import URLCreate, URLResponse, URLstats
from app.models.url import URL
from app.services.shortener import generate_short_code
from app.db.database import get_db
from app.services.shortener import generate_unique_short_code

router = APIRouter()


@router.post("/shorten", response_model=URLResponse, status_code=status.HTTP_201_CREATED)
def create_short_url(payload: URLCreate, db: Session = Depends(get_db)):
    short_code = generate_unique_short_code(db)

    while db.query(URL).filter(URL.short_code == short_code).first():
        short_code = generate_unique_short_code(db)
    url = URL(
        long_url=str(payload.long_url),
        short_code=short_code,
        access_count=0,
        expires_at=payload.expires_at
    )

    db.add(url)
    db.commit()
    db.refresh(url)

    return url

@router.get("/{short_code}")
def redirect_url(short_code: str, db: Session = Depends(get_db)):
    url = db.query(URL).filter(URL.short_code == short_code).first()

    if not url:
        raise HTTPException(status_code=404, detail="Short URL not found")

    if url.expires_at and url.expires_at < datetime.utcnow():
        raise HTTPException(status_code=410, detail="Short URL has expired")

    url.access_count += 1
    db.commit()

    return RedirectResponse(url=url.long_url)

@router.get("/stats/{short_code}", response_model=URLstats)
def get_url_stats(short_code: str, db: Session = Depends(get_db)):
    url = db.query(URL).filter(URL.short_code == short_code).first()

    if not url:
        raise HTTPException(status_code=404, detail="Short URL not found")

    return url