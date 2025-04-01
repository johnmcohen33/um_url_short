
from sqlmodel import select
from app.database import SessionDep
from app.models import ShortenedUrl
        
def get_all_short_urls(db: SessionDep):
    # TODO: Remove this method ! Just for DEV
    shortened_urls = db.exec(select(ShortenedUrl)).all()
    return shortened_urls

def create_short_url_db(long_url: str, unique_short_url: str, db: SessionDep) -> ShortenedUrl:
    new_url = ShortenedUrl(short_url=unique_short_url, long_url=long_url)
    db.add(new_url)
    db.commit()
    db.refresh(new_url)
    return new_url