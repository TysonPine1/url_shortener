import string
import random
from sqlalchemy.orm import Session
from app.models.url import URL
 
def generate_short_code(length: int = 6) -> str:
    characters = string.ascii_letters + string.digits
    return "".join(random.choice(characters) for _ in range(length))

def generate_unique_short_code(db: Session, length: int = 6) -> str:
    while True:
        short_code = generate_short_code(length)
        exisits = db.query(URL).filter(URL.short_code == short_code).first()
        if not exisits:
            return short_code