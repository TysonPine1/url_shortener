import string
import random
from sqlalchemy.orm import Session
from app.models.url import URL
 
def generate_short_code(length: int = 6) -> str:
    characters = string.ascii_letters + string.digits
    return "".join(random.choice(characters) for _ in range(length))

def generate_unique_short_code(db: Session, length: int = 6, max_attempts: int = 10) -> str:
    for _ in range(max_attempts):
        short_code = generate_short_code(length)
        exists = db.query(URL).filter(URL.short_code == short_code).first()
        if not exists:
            return short_code
    raise Exception("Failed to generate unique short code")