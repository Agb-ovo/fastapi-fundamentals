from pydantic import BaseModel
import json


class CarInput(BaseModel):
    size: str
    fuel: str | None = "electric"
    doors: int
    transmission: str | None = "auto"

class CarOutput(CarInput):
    id: int


#def load_db() -> list[Car]:
    """"Load a list of Car objects from a JSON file"""
    #with open("cars.json") as f:
        #return[Car.model_validate(obj) for obj in json.load(f)]

def load_db() -> list[CarOutput]:
    with open("cars.json") as f:
        car_data = json.load(f)
        return [CarOutput.model_validate(obj) for obj in car_data]

def save_db(cars: list[CarInput]):
    with open("cars.json", 'w') as f:
        json.dump([car.model_dump() for car in cars], f, indent=4)


