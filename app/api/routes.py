from fastapi import APIRouter, Depends, HTTPException, status
import fastapi.responses as RidrectResponse
from sqlalchemy.orm import Session

from app.schemas.url import URLCreate, URLResponse
from app.models.url import URL
from app.services.shortener import generate_short_code
from app.db.database import get_db

router = APIRouter()


@router.post("/shorten", response_model=URLResponse, status_code=status.HTTP_201_CREATED)
def create_short_url(payload: URLCreate, db: Session = Depends(get_db)):
    short_code = generate_short_code()

    while db.query(URL).filter(URL.short_code == short_code).first():
        short_code = generate_short_code()

    url = URL(
        long_url=str(payload.long_url),
        short_code=short_code,
        access_count=0
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

    url.access_count += 1
    db.commit()

    return RidrectResponse(url=url.long_url)