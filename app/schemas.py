from datetime import datetime
from pydantic import BaseModel, Field
from .database.models import ShipmentStatus


class BaseShipment(BaseModel):
    content: str
    weight: float | None = Field(le=25, default=None)
    destination: int


class ShipmentRead(BaseShipment):
    status: ShipmentStatus
    estimated_dilivery: datetime


class ShipmentCreate(BaseShipment):
    pass


class ShipmentUpdate(BaseModel):
    status: ShipmentStatus | None = Field(default=None)
    estimated_delivery: datetime | None = Field(default=None)
