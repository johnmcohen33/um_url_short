from typing import Optional
from sqlmodel import Field, SQLModel
from datetime import datetime

class ShortenedUrl(SQLModel, table=True):
    __tablename__ = "lu_shortened_urls"
    short_url: str = Field(primary_key=True)
    long_url: str
    expiration_date: Optional[datetime] = Field(default=None, nullable=True)