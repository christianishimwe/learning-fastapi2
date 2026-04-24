from datetime import datetime
from enum import Enum

from sqlmodel import Field, SQLModel


class ShipmentStatus(str, Enum):
    placed = "placed"
    shipped = "shipped"
    in_transit = "in_transit"


class Shipment(SQLModel, table=True):
    __tablename__ = "shipment"
    # none here allows us to create a new shipment without providing an id, and the database will auto-generate it
    id: int = Field(primary_key=True, default=None)
    content: str
    weight: float = Field(le=25)
    destinatio: int
    status: ShipmentStatus
    estimated_dilivery: datetime
