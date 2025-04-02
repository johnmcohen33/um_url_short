from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.database import init_db
from app.routes.url_shortener import url_shortener_router
from app.routes.auth import auth_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    This runs every time the app starts up.

    It initializes the database by creating tables for all models in `models.py`
    that inherit from SQLModel. This is super handy during development, but for
    production or evolving schemas, you'd probably want something like Alembic to properly
    manage migrations and keep your database in sync with code. 
    """
    init_db()
    yield

app = FastAPI(lifespan=lifespan)
app.include_router(url_shortener_router)
app.include_router(auth_router)