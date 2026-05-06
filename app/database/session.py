from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlmodel import Session, SQLModel
from sqlalchemy.orm import sessionmaker
from app.config import settings

engine = create_async_engine(
    url=settings.POSTGRES_URL,
    # log sql queries, this is useful for debugging and development, but should be turned off in production
    echo=True,
)


async def create_db_tables():
    # create all tables
    with engine.begin() as connection:
        await connection.run_sync(SQLModel.metadata.create_all)


async def get_session():
    # session has a context manager, so we can use it with a with statement
    """
    with AsyncSession(bind=engine) as session:
        yield session
    """
    async_session = sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )
    async with async_session() as session:
        yield session

SessionDep = Annotated[AsyncSession, Depends(get_session)]
