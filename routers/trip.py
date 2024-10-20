from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from crud import trip as trip_crud
from schemas import trip as trip_schemas
from db import get_db

router = APIRouter()

# Create a new trip
@router.post("/trips/", response_model=trip_schemas.TripOut)
def create_trip(trip: trip_schemas.TripCreate, db: Session = Depends(get_db)):
    return trip_crud.create_trip(db, trip)

# Get a trip by ID
@router.get("/trips/{trip_id}", response_model=trip_schemas.TripOut)
def read_trip(trip_id: int, db: Session = Depends(get_db)):
    db_trip = trip_crud.get_trip(db, trip_id)
    if db_trip is None:
        raise HTTPException(status_code=404, detail="Trip not found")
    return db_trip

# Get trips by driver ID
@router.get("/trips/driver/{user_id}", response_model=list[trip_schemas.TripOut])
def get_trips_by_driver(user_id: int, db: Session = Depends(get_db)):
    return trip_crud.get_trips_by_driver(db, user_id)

# Update a trip
@router.put("/trips/{trip_id}", response_model=trip_schemas.TripOut)
def update_trip(trip_id: int, trip_update: trip_schemas.TripUpdate, db: Session = Depends(get_db)):
    db_trip = trip_crud.update_trip(db, trip_id, trip_update)
    if db_trip is None:
        raise HTTPException(status_code=404, detail="Trip not found")
    return db_trip

# Delete a trip
@router.delete("/trips/{trip_id}", response_model=trip_schemas.TripOut)
def delete_trip(trip_id: int, db: Session = Depends(get_db)):
    db_trip = trip_crud.delete_trip(db, trip_id)
    if db_trip is None:
        raise HTTPException(status_code=404, detail="Trip not found")
    return db_trip
