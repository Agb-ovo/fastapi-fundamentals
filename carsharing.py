from fastapi import FastAPI
from datetime import datetime

from schemas import load_db,Car,save_db

app = FastAPI()

db = load_db()

@app.get("/")
def welcome(name):
    """"Return a friendly welcome message"""
    return {'message': f"Welcome {name} to the Car sharing service"}


@app.get("/date")
def date():
    """"Return a friendly welcome message"""
    return {'date': datetime.now()}

@app.get("/api/cars")
def get_cars(size: str|None = None, doors: int|None = None) -> list:
# def get_cars(size: Optional[str] = None, doors: Optional[str] = None) -> List:
    result = db
    if size:
        result = [car for car in result if car.size == size]
    if doors:
        result = [car for car in result if car.doors >= doors]
    return result


@app.get("/api/cars/{id}")
def car_by_id(id: int):
    result = [car for car in db if car.id == id]
    return result[0]

@app.post("/api/cars/")
def add_car(car: Car):
    db.append(car)
    save_db(db)








