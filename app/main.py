from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.database import init_db
from app.routes.url_shortener import url_shortener_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(lifespan=lifespan)
app.include_router(url_shortener_router)