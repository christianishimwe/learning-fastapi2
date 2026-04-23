from enum import Enum
from pydantic import BaseModel, Field
from typing import Optional, Literal
import datetime


class ShipmentStatus(str, Enum):
    pending = "pending"
    shipped = "shipped"
    delivered = "delivered"


class ShipmentBase(BaseModel):
    shipment_id: str


class ShipmentCreate(ShipmentBase):
    status: Literal[ShipmentStatus.pending] = ShipmentStatus.pending
    recipient_address: str
    expected_delivery_date: str


class ShipmentUpdate(BaseModel):
    # Make all fields from ShipmentCreate optional
    shipment_id: Optional[str] = None
    # Allow any valid status, and make it optional
    status: Optional[ShipmentStatus] = None
    recipient_address: Optional[str] = None
    expected_delivery_date: Optional[str] = None
    updated_at: str = Field(
        default_factory=lambda: datetime.datetime.now().isoformat())


class ShipmentResponse(BaseModel):
    id: int
    shipment_id: str
    # Allow any valid status, and make it optional
    status: ShipmentStatus
    recipient_address: str
    expected_delivery_date: str
    updated_at: str
