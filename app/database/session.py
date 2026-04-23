from sqlalchemy import create_engine
from sqlmodel import SQLModel

engine = create_engine(
    url="",
    echo=True,
)


def create_db_tables():
    # create all tables
    SQLModel.metadata.create_all(bind=engine)
