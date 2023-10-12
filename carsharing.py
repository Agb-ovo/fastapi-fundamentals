from fastapi import FastAPI
from datetime import datetime

from schemas import load_db,CarInput,save_db , CarOutput

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

@app.post("/api/cars/", response_model=CarOutput)
def add_car(car: CarInput) -> CarOutput:
    new_car = CarOutput(size=car.size, doors=car.doors, fuel=car.fuel, transmission=
                        car.transmission, id=len(db)+1)
    db.append(new_car)
    save_db(db)
    return new_car

@app.delete("/api/cars/{id}", status_code=204)
def remove_car(id: int) -> None:
    matches = [car for car in db if car.id == id]
    if matches:
        car = matches[0]
        db.remove(car)
        save_db(db)
    else:
        raise HTTPException(status_code=404, detail=f"No car with id={id}.")

@app.put("/api/cars/{id}", response_model=CarOutput)
def change_car(id: int, new_data: CarInput) -> CarOutput:
    matches = [car for car in db if car.id == id]
    if matches:
        car = matches[0]
        car.fuel = new_data.fuel
        car.transmission = new_data.transmission
        car.size = new_data.size
        car.doors = new_data.doors
        save_db(db)
        return car
    else:
        raise HTTPException(status_code=404, detail=f"No car with id={id}.")








