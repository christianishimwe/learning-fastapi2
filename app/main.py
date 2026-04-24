from contextlib import asynccontextmanager
from datetime import datetime, timedelta

from fastapi import FastAPI, HTTPException, status
from rich import panel, print

from app.database.session import SessionDep, create_db_tables

from . import schemas
from .database import models


@asynccontextmanager
async def lifespan_handler(app: FastAPI):
    print(panel.Panel("Server started..", border_style="green"))
    # create the database tables here
    create_db_tables()
    yield
    print(panel.Panel("Server stopped..", border_style="red"))


app = FastAPI(lifespan=lifespan_handler)


@app.get("/shipments", response_model=schemas.BaseShipment)
def get_shipments(incoming_shipment: schemas.BaseShipment, session: SessionDep) -> dict:
    ''''
    Notice how we used Depends to inject the database session into our endpoint, this allows us to use the session to interact with the database and perform CRUD operations on the shipments table.
    insted if we just used session = get_session(), this would be given a value at function defintion time, but
    we won't be able to get the cleanups, yields will not work well since the function will no longer be a generator, and we won't be able to use the context manager to manage the database connection, this is why we use Depends to inject the session into our endpoint, this allows us to use the session as a dependency and get the benefits of the context manager and yields.
    '''
    # create a new shipment dictionary
    new_shipment = {
        "content": incoming_shipment.content,
        "weight": incoming_shipment.weight,
        "destination": incoming_shipment.destination,
        "status": "in transit"
    }
    # replace it with the incoming shipment,
    # by transforming the incoming shipemnet to a dictionary and then unpacking it
    new_shipment = {
        **incoming_shipment.model_dump(),
        "status": "in transit",
    }
    return new_shipment


@app.patch("/shipments/", response_model=schemas.ShipmentRead)
def update_shipment(shipment_id: int, incoming_shipment: schemas.ShipmentUpdate, session: SessionDep):
    # create a new shipment dictionary
    update = incoming_shipment.model_dump(exclude_none=True)
    # if all the vaoues are none
    if not update:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="No values to update")
    shipment = session.get(models.Shipment, shipment_id)
    if shipment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Shipment not found")
    shipment.sqlmodel_update(update)
    # replace it with the incoming shipment,

    # by transforming the incoming shipemnet to a dictionary and then unpacking it
    # but we want to onlly set values which are not none
    # now add it to the session
    session.add(shipment)
    session.commit()
    session.refresh(shipment)

    return shipment


@app.delete("/shipements/{shipment_id}", response_model=None)
def delete_shipment(shipment_id: int, session: SessionDep):
    shipment = session.get(models.Shipment, shipment_id)
    if shipment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Shipment not found")
    session.delete(shipment)
    session.commit()


@app.post("/shipment", response_model=None)
def submit_shipment(incoming_shipment: schemas.ShipmentCreate, session: SessionDep) -> dict[str, int]:
    new_shipment = models.Shipment(
        **incoming_shipment.model_dump(),
        status=models.ShipmentStatus.placed,
        estimated_delivery=datetime.now() + timedelta(days=7)
    )
    # let's grab the sesssion and add the new shipment to the database, then commit the transaction
    session.add(new_shipment)
    session.commit()

    # get the id that got created in the database
    session.refresh(new_shipment)
    return {"id": new_shipment.id}
