from contextlib import asynccontextmanager

from fastapi import FastAPI
from rich import panel, print

from app.database.session import create_db_tables

from app.api.router import master_router

@asynccontextmanager
async def lifespan_handler(app: FastAPI):
    print(panel.Panel("Server started..", border_style="green"))
    # create the database tables here
    await create_db_tables()
    yield
    print(panel.Panel("Server stopped..", border_style="red"))


app = FastAPI(lifespan=lifespan_handler)

app.include_router(master_router)


@app.get("/")
def root():
    return {"message": "Hello World"}
