from uuid import UUID
from fastapi import APIRouter, HTTPException, status
from app.api.dependencies import DeliveryPartnerDep, SellerDep, ShipmentServiceDep
from app.database import models
from app.services.shipment import ShipmentService
from ..schemas import shipment

router = APIRouter(prefix="/shipment",
                   tags=["shipment"])


@router.get("/", response_model=shipment.ShipmentRead)
async def get_shipments(id: UUID, service: ShipmentServiceDep, seller: SellerDep):
    ''''
    Notice how we used Depends to inject the database session into our endpoint, this allows us to use the session to interact with the database and perform CRUD operations on the shipments table.
    insted if we just used session = get_session(), this would be given a value at function defintion time, but
    we won't be able to get the cleanups, yields will not work well since the function will no longer be a generator, and we won't be able to use the context manager to manage the database connection, this is why we use Depends to inject the session into our endpoint, this allows us to use the session as a dependency and get the benefits of the context manager and yields.
    '''
    # check for the shipment with the given id
    shipment = await service.get(id)

    if shipment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Shipment not found")
    return shipment


@router.post("/", status_code=status.HTTP_201_CREATED)
async def submit_shipment(incoming_shipment: shipment.ShipmentCreate, service: ShipmentServiceDep, seller: SellerDep) -> models.Shipment:
    shipment = await service.add(incoming_shipment, seller)
    return shipment

# update shipment
# should only be accessible to allowed delivery partners


@router.patch("/", response_model=shipment.ShipmentRead)
async def update_shipment(
        id: UUID,
        shipment_update: shipment.ShipmentUpdate,
        partner: DeliveryPartnerDep,
        service: ShipmentServiceDep,
):
    update = shipment_update.model_dump(exclude_none=True)
    if not update:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="no data provided to update"
        )

    return await service.update(id, shipment_update, partner)

# cancel a shipment by id


@router.get("/cancel", response_model=shipment.ShipmentRead)
async def cancel_shipment(id: UUID, seller: SellerDep, service: ShipmentServiceDep):
    return await service.cancel(id, seller)
