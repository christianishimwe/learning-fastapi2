from datetime import datetime
from pydantic import BaseModel, Field
from uuid import UUID
from app.api.schemas.seller import SellerRead
from app.database.models import Seller, ShipmentEvent, ShipmentStatus


class BaseShipment(BaseModel):
    content: str
    weight: float | None = Field(le=25, default=None)
    destination: int


class ShipmentRead(BaseShipment):
    id: UUID
    timeline: list[ShipmentEvent]
    estimated_delivery: datetime
    seller: SellerRead


class ShipmentCreate(BaseShipment):
    pass


class ShipmentUpdate(BaseModel):
    location: int | None = Field(default=None)
    description: str | None = Field(default=None)
    status: ShipmentStatus | None = Field(default=None)
    estimated_delivery: datetime | None = Field(default=None)
