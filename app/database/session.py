from typing import Annotated

from fastapi import Depends
from sqlalchemy import create_engine
from sqlmodel import Session, SQLModel

engine = create_engine(
    url="",
    echo=True,
)


def create_db_tables():
    # create all tables
    SQLModel.metadata.create_all(bind=engine)


def get_session():
    # session has a context manager, so we can use it with a with statement
    with Session(bind=engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]
