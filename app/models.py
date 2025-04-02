from typing import Optional
from pydantic import BaseModel
from sqlmodel import Field, SQLModel
from datetime import datetime, timezone

class ShortenedUrl(SQLModel, table=True):
    __tablename__ = "lu_shortened_urls"
    short_url: str = Field(primary_key=True)
    long_url: str
    expiration_date: Optional[datetime] = Field(default=None, nullable=True)

class User(SQLModel, table=True):
    """
    Declares a SQLModel-backed database table.

    Setting `table=True` tells SQLModel (and FastAPI) to create a corresponding table
    in the database for this model. In production, you’d typically use a migration tool
    like Alembic to manage schema changes instead of relying on auto-creation.
    """
    username: str = Field(primary_key=True)
    email: str | None = None
    hashed_password: str
    full_name: str | None = None
    disabled: bool | None = None
    creation_date: Optional[datetime] = Field(default=datetime.now(timezone.utc), nullable=True)

class UserCreate(BaseModel):
    """
    Pydantic model for user creation input.

    This model is used to validate and document the data required
    when creating a new user. It includes the plain text password
    (which should be hashed before storing). Swagger docs are auto-
    generated from this thanks to Pydantic + FastAPI integration.
    """
    username: str
    email: str
    full_name: str
    password: str  # plain text password, not stored!

class UserPublic(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    creation_date: datetime

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None