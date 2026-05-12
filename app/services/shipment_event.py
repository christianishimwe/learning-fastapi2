from app.database.models import Shipment, ShipmentEvent, ShipmentStatus
from app.services.base import BaseService


class ShipmnentEventService(BaseService):
    def __init__(self, session):
        super().__init__(ShipmentEvent, session)

    async def add(
        self,
        shipment: Shipment,
        location: int | None = None,
        status: ShipmentStatus | None = None,
        description: str | None = None,
    ) -> ShipmentEvent:
        # if the location is not provided, find the laterst event's location
        if not location or not status:
            last_event = await self.get_latest_event(shipment)
            location = location if location else last_event.location
            status = status if status else last_event.status

        if not status:
            last_event = await self.get_latest_event(shipment)
            status = last_event.status

        new_event = ShipmentEvent(
            location=location,
            status=status,
            description=description if description else self._generate_description(
                status, location),
            shipment_id=shipment.id
        )
        return await self._add(new_event)

    async def get_latest_event(self, shipment: Shipment):
        timeline = shipment.timeline
        timeline.sort(key=lambda event: event.created_at)
        return timeline[-1]

    def _generate_description(self, status: ShipmentStatus | None, location: int):
        match status:
            case ShipmentStatus.placed:
                return "assigned delivery partner"
            case ShipmentStatus.shipped:
                return "shipment is shipped"
            case ShipmentStatus.in_transit:
                return "shipment is in transit"
            case ShipmentStatus.delivered:
                return "successfully delivered"
            case ShipmentStatus.cancelled:
                return "cancelled by the seller"
            case _:
                return f"scanned at {location}"
