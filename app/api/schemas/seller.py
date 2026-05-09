
from uuid import UUID
from pydantic import BaseModel, EmailStr

from app.database.models import Shipment


class BaseSeller(BaseModel):
    name: str
    email: EmailStr


class SellerRead(BaseSeller):
    id: UUID
    shipments: list[Shipment]


class SellerCreate(BaseSeller):
    password: str
