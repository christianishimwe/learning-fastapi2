
from uuid import UUID
from pydantic import BaseModel, EmailStr

from app.database.models import Shipment


class BaseDeliveryPartner(BaseModel):
    name: str
    email: EmailStr
    serviceable_zip_codes: list[int]
    max_handling_capacity: int


class DeliveryPartnerRead(BaseDeliveryPartner):
    id: UUID
    shipments: list[Shipment]


class DeliveryPartnerUpdate(BaseModel):
    serviceable_zip_codes: list[int]
    max_handling_capacity: int


class DeliveryPartnerCreate(BaseDeliveryPartner):
    password: str
