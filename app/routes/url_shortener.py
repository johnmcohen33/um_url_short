from fastapi import APIRouter
from sqlmodel import select
from app.crud.url_shortener import create_short_url_db, get_all_short_urls
from app.models import ShortenedUrl

from app.database import SessionDep
from app.config import settings

import shortuuid

url_shortener_router = APIRouter()

@url_shortener_router.get('/')
async def root():
    return {"message": "url_shortener_router root"}

def generate_unique_id(db_session: SessionDep) -> str:
    """ gurantees a unique id from the database. """
    while True:
        new_short_id = shortuuid.uuid()[:7] # 7 characters ~= 2 trillion unique urls
        exists = db_session.exec(select(ShortenedUrl).where(ShortenedUrl.short_url == new_short_id)).first()

        if not exists:
            return new_short_id
        
@url_shortener_router.post("/shorten/")
async def create_short_url(long_url: str, db_session: SessionDep):
    unique_short_id = generate_unique_id(db_session)
    create_short_url_db(long_url=long_url, unique_short_url=unique_short_id, db=db_session)
    return {"message": f"new short_url created! Here it is: {settings.BASE_URL}/{unique_short_id}"}

@url_shortener_router.get("/urls/")
async def get_short_urls(db_session: SessionDep):
    # TODO: Remove ! This is just for DEV!
    return get_all_short_urls(db_session)