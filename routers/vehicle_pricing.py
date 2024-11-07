# routers/vehicle_pricing.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db import get_db
from crud import vehicle_pricing as vehicle_pricing_crud
from schemas.vehicle_pricing import VehiclePricingCreate, VehiclePricingOut
from typing import List

router = APIRouter()

@router.post("/vehicle_pricing/", response_model=VehiclePricingOut)
def create_vehicle_pricing(vehicle_pricing: VehiclePricingCreate, db: Session = Depends(get_db)):
    db_vehicle = vehicle_pricing_crud.get_vehicle_pricing_by_type(db, vehicle_pricing.vehicle_type)
    if db_vehicle:
        raise HTTPException(status_code=400, detail="Vehicle type already exists")
    return vehicle_pricing_crud.create_vehicle_pricing(db=db, vehicle_pricing=vehicle_pricing)

@router.get("/vehicle_pricings/", response_model=List[VehiclePricingOut])
def read_vehicle_pricings(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return vehicle_pricing_crud.get_vehicle_pricings(db, skip=skip, limit=limit)