
from uuid import UUID
from pydantic import BaseModel, EmailStr, Field

from app.database.models import Shipment


class BaseSeller(BaseModel):
    name: str
    email: EmailStr


class SellerRead(BaseSeller):
    id: UUID
    zip_code: int


class SellerCreate(BaseSeller):
    password: str
    zip_code: int
    address: str | None = Field(default=None)
