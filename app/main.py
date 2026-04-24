from fastapi import FastAPI, Depends
from . import schemas
from contextlib import asynccontextmanager
from rich import print, panel
from app.database.session import create_db_tables, get_session
from sqlmodel import Session


@asynccontextmanager
async def lifespan_handler(app: FastAPI):
    print(panel.Panel("Server started..", border_style="green"))
    # create the database tables here
    create_db_tables()
    yield
    print(panel.Panel("Server stopped..", border_style="red"))


app = FastAPI(lifespan=lifespan_handler)


@app.get("/shipments", response_model=schemas.BaseShipment)
def get_shipments(incoming_shipment: schemas.BaseShipment, session: Session = Depends(get_session)) -> dict:
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


@app.patch("/shipments/{shipment_id}", response_model=schemas.BaseShipment)
def update_shipment(shipment_id: int, incoming_shipment: schemas.BaseShipment, session: Session = Depends(get_session)) -> dict:
    # create a new shipment dictionary
    new_shipment = {
        "content": "wood",
        "weight": 20.0,
        "destination": 123,
        "status": "in transit"
    }
    # replace it with the incoming shipment,

    # by transforming the incoming shipemnet to a dictionary and then unpacking it
    # but we want to onlly set values which are not none
    new_shipment.update(
        **incoming_shipment.model_dump(exclude_none=True), status="in transit")
    return new_shipment
