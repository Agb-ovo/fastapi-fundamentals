from fastapi import Depends, HTTPException, APIRouter
from sqlmodel import Session, select

from db import get_session
from schemas import Car, CarInput, CarOutput, Trip, TripInput

router = APIRouter()


@router.get("/api/cars")
def get_cars(size: str | None = None, doors: int | None = None,
             session: Session = Depends(get_session)) -> list:
    query = select(Car)
    if size:
        query = query.where(Car.size == size)
    if doors:
        query = query.where(Car.doors >= doors)
    return session.exec(query).all()


@router.get("/api/cars/{id}", response_model=CarOutput)
def car_by_id(id: int, session: Session = Depends(get_session)) -> Car:
    car = session.get(Car, id)
    if car:
        return car
    else:
        raise HTTPException(status_code=404, detail=f"No car with id={id}.")


@router.get("/")
def welcome(name):
    """"Return a friendly welcome message"""
    return {'message': f"Welcome {name} to the Car sharing service"}


@router.get("/date")
def date():
    """"Return a friendly welcome message"""
    return {'date': datetime.now()}


@router.get("/api/cars")
def get_cars(size: str|None = None, doors: int|None = None) -> list:
    # def get_cars(size: Optional[str] = None, doors: Optional[str] = None) -> List:
    result = db
    if size:
        result = [car for car in result if car.size == size]
    if doors:
        result = [car for car in result if car.doors >= doors]
    return result


#@app.get("/api/cars/{id}")
#def car_by_id(id: int):
    #result = [car for car in db if car.id == id]
    #return result[0]


@router.post("/api/cars/", response_model=Car)
def add_car(car_input: CarInput, session: Session = Depends(get_session)) -> Car:
    new_car = Car.from_orm(car_input)
    session.add(new_car)
    session.commit()
    session.refresh(new_car)
    return new_car


@router.delete("/api/cars/{id}", status_code=204)
def remove_car(id: int, session: Session = Depends(get_session)) -> None:
    car = session.get(Car, id)
    if car:
        session.delete(car)
        session.commit()
    else:
        raise HTTPException(status_code=404, detail=f"No car with id={id}.")


@router.delete("/api/cars/{id}", status_code=204)
def remove_car(id: int) -> None:
    matches = [car for car in db if car.id == id]
    if matches:
        car = matches[0]
        db.remove(car)
        save_db(db)
    else:
        raise HTTPException(status_code=404, detail=f"No car with id={id}.")


@router.put("/api/cars/{id}", response_model=CarOutput)
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


@router.put("/api/cars/{id}", response_model=Car)
def change_car(id: int, new_data: CarInput,
               session: Session = Depends(get_session)) -> Car:
    car = session.get(Car, id)
    if car:
        car.fuel = new_data.fuel
        car.transmission = new_data.transmission
        car.size = new_data.size
        car.doors = new_data.doors
        session.commit()
        return car
    else:
        raise HTTPException(status_code=404, detail=f"No car with id={id}.")


@router.post("/api/cars/{car_id}/trips", response_model=Trip)
def add_trip(car_id: int, trip_input: TripInput,
             session: Session = Depends(get_session)) -> Trip:
    car = session.get(Car, car_id)
    if car:
        new_trip = Trip.from_orm(trip_input, update={'car_id': car_id})
        car.trips.append(new_trip)
        session.commit()
        session.refresh(new_trip)
        return new_trip
    else:
        raise HTTPException(status_code=404, detail=f"No car with id={id}.")



