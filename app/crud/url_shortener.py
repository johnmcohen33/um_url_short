
from sqlmodel import select
from app.database import SessionDep
from app.models import ShortenedUrl
        
def get_all_short_urls_db(db: SessionDep):
    """ WARNING: THIS IS NOT A GOOD METHOD! IT'S JUST FOR US TO TEST EASILY ! """
    # TODO: Remove this method ! Just for DEV
    shortened_urls = db.exec(select(ShortenedUrl)).all()
    return shortened_urls

def create_short_url_db(long_url: str, unique_short_url: str, db: SessionDep) -> ShortenedUrl:
    """ 
    Adds a new short url to the DB. 
    NOTE: Assumes unique_short_url is pre-validated. 
    Uniqueness is enforced outside the CRUD layer to keep responsibilities separated.
    """
    new_url = ShortenedUrl(short_url=unique_short_url, long_url=long_url)
    db.add(new_url)
    db.commit()
    db.refresh(new_url)
    return new_url

def get_redirect_url_db(short_id: str, db_session: SessionDep) -> ShortenedUrl:
    """
    Gets the ShortenedUrl object from the database.
    """
    return db_session.exec(select(ShortenedUrl).where(ShortenedUrl.short_url == short_id)).first()
