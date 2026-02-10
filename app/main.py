from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from app.db.database import engine, Base
from app.models import url
from app.api.routes import router 


app = FastAPI(
    title="URL shortener service",
    description="A simple URL shortener service built with FastAPI.",
    version="1.0.0"
)

Base.metadata.create_all(bind=engine)
app.include_router(router)

@app.get("/")
def root():
    return RedirectResponse(url="/docs")

