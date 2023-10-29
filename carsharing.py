from fastapi import FastAPI
from sqlmodel import SQLModel

from db import engine
from routers import cars

app = FastAPI(title="Car Sharing")
app.include_router(cars.router)


@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)















