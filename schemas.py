from pydantic import BaseModel
import json


class Car(BaseModel):
    id: int
    size: str
    fuel: str | None = "electric"
    doors: int
    transmission: str | None = "auto"


#def load_db() -> list[Car]:
    """"Load a list of Car objects from a JSON file"""
    #with open("cars.json") as f:
        #return[Car.model_validate(obj) for obj in json.load(f)]

def load_db() -> list[Car]:
    with open("cars.json") as f:
        car_data = json.load(f)
        return [Car.model_validate(obj) for obj in car_data]


