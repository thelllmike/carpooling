from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from crud import passenger as passenger_crud
from schemas import passenger as passenger_schemas
from db import get_db

router = APIRouter()

@router.post("/passengers/", response_model=passenger_schemas.PassengerOut)
def create_passenger(passenger: passenger_schemas.PassengerCreate, db: Session = Depends(get_db)):
    return passenger_crud.create_passenger(db, passenger)

@router.get("/passengers/{passenger_id}", response_model=passenger_schemas.PassengerOut)
def read_passenger(passenger_id: int, db: Session = Depends(get_db)):
    db_passenger = passenger_crud.get_passenger(db, passenger_id)
    if db_passenger is None:
        raise HTTPException(status_code=404, detail="Passenger not found")
    return db_passenger

@router.delete("/passengers/{passenger_id}", response_model=passenger_schemas.PassengerOut)
def delete_passenger(passenger_id: int, db: Session = Depends(get_db)):
    db_passenger = passenger_crud.delete_passenger(db, passenger_id)
    if db_passenger is None:
        raise HTTPException(status_code=404, detail="Passenger not found")
    return db_passenger
