from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from crud import vehicle as vehicle_crud
from schemas import vehicle as vehicle_schemas
from db import get_db

router = APIRouter()

@router.post("/vehicles/", response_model=vehicle_schemas.VehicleOut)
def create_vehicle(vehicle: vehicle_schemas.VehicleCreate, db: Session = Depends(get_db)):
    return vehicle_crud.create_vehicle(db, vehicle)

@router.get("/vehicles/{vehicle_id}", response_model=vehicle_schemas.VehicleOut)
def read_vehicle(vehicle_id: int, db: Session = Depends(get_db)):
    db_vehicle = vehicle_crud.get_vehicle(db, vehicle_id)
    if db_vehicle is None:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    return db_vehicle

@router.get("/vehicles/user/{user_id}", response_model=list[vehicle_schemas.VehicleOut])
def read_vehicles_by_user(user_id: int, db: Session = Depends(get_db)):
    return vehicle_crud.get_vehicles_by_user(db, user_id)

@router.delete("/vehicles/{vehicle_id}", response_model=vehicle_schemas.VehicleOut)
def delete_vehicle(vehicle_id: int, db: Session = Depends(get_db)):
    db_vehicle = vehicle_crud.delete_vehicle(db, vehicle_id)
    if db_vehicle is None:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    return db_vehicle
