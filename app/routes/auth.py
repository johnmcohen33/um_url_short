"""
NOTE: This authentication logic is largely adapted from the official FastAPI tutorial:
https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/

I didn’t write most of this from scratch — instead, I pulled it in so we could simulate
a working auth system and see how data can be scoped to actual users. This let me hook
real user accounts into parts of the app while demonstrating my ability to quickly read,
understand, and integrate FastAPI’s documentation and examples.

My additions are minimal and focused on connecting the core logic to our project’s needs.
"""

from typing import Annotated

from datetime import datetime, timezone, timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import jwt
from passlib.context import CryptContext
from sqlmodel import select
from app.database import SessionDep
from app.models import Token, TokenData, User, UserCreate, UserPublic

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# TODO: probably not great to store here lol
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

auth_router = APIRouter()

def get_password_hash(password: str):
    """ Hash a plain password """
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str):
    """ Use library to verify if a received password matches the hash stored """
    return pwd_context.verify(plain_password, hashed_password)

def authenticate_user(db_session, username: str, password: str):
    """ Returns if a user is in the db """
    user = get_user(db_session, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

@auth_router.post("/token")
async def login_for_access_token(
    db_session: SessionDep,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    user = authenticate_user(db_session, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


def get_current_user(db_session: SessionDep, token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except jwt.InvalidTokenError:
        raise credentials_exception

    user = get_user(db_session, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

def get_user(db_session: SessionDep, username: str):
    user = db_session.exec(select(User).where(User.username == username)).first()
    if user:
        return user

@auth_router.post('/users/', response_model=UserPublic)
async def create_user(user_create: UserCreate, db_session: SessionDep):
    # Check if user already exists
    existing_user = db_session.exec(select(User).where(User.username == user_create.username)).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")
    
    new_user = User(
        username=user_create.username,
        email=user_create.email,
        full_name=user_create.full_name,
        hashed_password=get_password_hash(user_create.password),
    )

    db_session.add(new_user)
    db_session.commit()
    db_session.refresh(new_user)
    return UserPublic(username=new_user.username, email=new_user.email, full_name=new_user.full_name, creation_date=new_user.creation_date)

# This is the dependency we inject into protected routes to access the current authenticated user.
# It ensures the user is both authenticated and active before allowing access.
UserDep = Annotated[User, Depends(get_current_active_user)]