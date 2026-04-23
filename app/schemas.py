from pydantic import BaseModel, Field


class BaseShipment(BaseModel):
    content: str
    weight: float | None = Field(le=25, default=None)
    destination: int
