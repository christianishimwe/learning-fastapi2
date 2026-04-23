from sqlalchemy import create_engine
from sqlmodel import SQLModel
from .models import Shipment

engine = create_engine(
    url="",
    echo=True,
)

# create all tables
SQLModel.metadata.create_all(bind=engine)
