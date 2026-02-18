from dotenv import load_dotenv
import os

load_dotenv()

ENV = os.getenv("ENV", "local")

if ENV == "docker":
    DATABASE_URL = "postgresql://postgres:postgres@db:5432/url_shortener"
else:
    DATABASE_URL = "postgresql://postgres:vertin1999@localhost:5432/url_shortener"
# DATABASE_URL = os.getenv("DATABASE_URL")
