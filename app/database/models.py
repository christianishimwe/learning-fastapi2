from sqlmodel import SQLModel, Field
from enum import Enum
from datetime import datetime


class ShipmentStatus(str, Enum):
    pending = "pending"
    shipped = "shipped"
    in_transit = "in_transit"


class Shipment(SQLModel):
    __tablename__ = "shipment"
    id: int
    content: str
    weight: float = Field(le=25)
    destinatio: int
    status: ShipmentStatus
    estimated_dilivery: datetime
