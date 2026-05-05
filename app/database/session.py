from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel import Session, SQLModel
from app.config import settings

engine = create_async_engine(
    url=settings.POSTGRES_URL,
    # log sql queries, this is useful for debugging and development, but should be turned off in production
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
