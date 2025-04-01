from fastapi import APIRouter, HTTPException
from fastapi.responses import RedirectResponse
from sqlmodel import select
from app.crud.url_shortener import create_short_url_db, get_all_short_urls_db, get_redirect_url_db
from app.models import ShortenedUrl

from app.database import SessionDep
from app.config import settings

import shortuuid

url_shortener_router = APIRouter()

def generate_unique_id(db_session: SessionDep) -> str:
    """ 
    Generates a unique 7-character short ID using shortuuid library.
    Ensures uniqueness by checking for collisions in the database.
    NOTE: This should probably be a utility or seperate class if we want to easily update how we create this.
    """
    while True:
        new_short_id = shortuuid.uuid()[:7] # 7 characters ~= 2 trillion unique urls
        exists = db_session.exec(select(ShortenedUrl).where(ShortenedUrl.short_url == new_short_id)).first()

        if not exists:
            return new_short_id
        
@url_shortener_router.post("/shorten/")
async def create_short_url(long_url: str, db_session: SessionDep):
    """
    Create a new shortened URL entry in the database.

    Args:
        long_url (str): The original URL to be shortened.
        db_session (SessionDep): The database session dependency.

    Returns:
        dict: A success message containing the newly generated short URL.
    """
    unique_short_id = generate_unique_id(db_session)
    create_short_url_db(long_url=long_url, unique_short_url=unique_short_id, db=db_session)
    return {"message": f"new short_url created! Here it is: {settings.BASE_URL}/{unique_short_id}"}

@url_shortener_router.get('/{short_id}')
async def redirect_url(short_id: str, db_session: SessionDep):
    """
    Redirect to the original URL associated with a given short ID.

    Args:
        short_id (str): The unique identifier for the shortened URL.
        db_session (SessionDep): The database session dependency.

    Returns:
        RedirectResponse: A temporary redirect to the original long URL.

    Raises:
        HTTPException: If the short ID is not found in the database.
    """
    url_entry = get_redirect_url_db(short_id=short_id, db_session=db_session)
    if not url_entry:
        raise HTTPException(status_code=404, detail=f"{short_id} could not be found.")
    return RedirectResponse(url=url_entry.long_url, status_code=301) # temporary redirect

@url_shortener_router.get("/urls/")
async def get_short_urls(db_session: SessionDep):
    """ WARNING: THIS IS NOT A GOOD METHOD! IT'S JUST FOR US TO TEST EASILY ! """
    # TODO: Remove this method ! Just for DEV
    return get_all_short_urls_db(db_session)