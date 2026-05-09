from datetime import datetime
from enum import Enum

from pydantic import EmailStr
from sqlalchemy import Column
from sqlmodel import Field, Relationship, SQLModel
from uuid import uuid4, UUID
from sqlalchemy.dialects import postgresql


class ShipmentStatus(str, Enum):
    placed = "placed"
    shipped = "shipped"
    in_transit = "in_transit"


class Shipment(SQLModel, table=True):
    __tablename__ = "shipment"
    # none here allows us to create a new shipment without providing an id, and the database will auto-generate it
    id: UUID = Field(
        sa_column=Column(
            postgresql.UUID,
            default=uuid4,
            primary_key=True
        )
    )
    content: str
    weight: float = Field(le=25)
    destination: int
    status: ShipmentStatus
    estimated_delivery: datetime
    seller_id: UUID = Field(foreign_key="seller.id")
    seller: "Seller" = Relationship(
        back_populates="shipments",
        sa_relationship_kwargs={"lazy": "selectin"}
    )


class Seller(SQLModel, table=True):
    __tablename__ = "seller"
    id: UUID = Field(
        sa_column=Column(
            postgresql.UUID,
            default=uuid4,
            primary_key=True
        )
    )
    name: str
    email: EmailStr
    address: int
    password_hash: str
    shipments: list[Shipment] = Relationship(
        back_populates="seller",
        sa_relationship_kwargs={"lazy": "selectin"}
    )
