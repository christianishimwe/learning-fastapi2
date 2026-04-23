from fastapi import FastAPI
from . import schemas


app = FastAPI()


@app.get("/shipments", response_model=schemas.BaseShipment)
def get_shipments(incoming_shipment: schemas.BaseShipment) -> dict:
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
def update_shipment(shipment_id: int, incoming_shipment: schemas.BaseShipment) -> dict:
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
