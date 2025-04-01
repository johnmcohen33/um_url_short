from typing import Annotated
from fastapi import Depends
from sqlmodel import SQLModel, Session, create_engine

DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Dependency to get DB session
def get_db():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_db)]

# Function to create all of the tables related to SQLModels
def init_db():
    SQLModel.metadata.create_all(engine)