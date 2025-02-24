from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app_models.booking import RideBooking
from app_models.passenger import Passenger
from app_models.trip import Trip
from app_models.user import User
from app_models.vehicle import Vehicle
from crud import trip as trip_crud
from schemas import trip as trip_schemas
from db import get_db

router = APIRouter()

@router.get("/trips/rider/{user_id}", response_model=List[trip_schemas.TripDetailOut])
def get_trips_by_rider(user_id: int, db: Session = Depends(get_db)):
    # Step 1: Find all Passenger records for the given rider (user)
    passenger_records = db.query(Passenger).filter(Passenger.user_id == user_id).all()
    if not passenger_records:
        raise HTTPException(status_code=404, detail="No passenger records found for this user.")
    
    # Step 2: Extract unique trip IDs from these passenger records
    trip_ids = list({record.trip_id for record in passenger_records})
    
    # Step 3: Retrieve trip details joined with driver and vehicle information
    trips_with_details = (
        db.query(
            Trip,
            User.full_name,
            User.profile_picture,
            Vehicle.vehicle_type,
            Vehicle.image_link,
        )
        .join(User, Trip.user_id == User.id)
        .join(Vehicle, Trip.vehicle_id == Vehicle.id)
        .filter(Trip.id.in_(trip_ids))
        .all()
    )
    
    if not trips_with_details:
        raise HTTPException(status_code=404, detail="No trips found for the given passenger records.")
    
    # Step 4: Map the results to the TripDetailOut schema
    results = []
    for trip, full_name, profile_picture, vehicle_type, image_link in trips_with_details:
        results.append(
            trip_schemas.TripDetailOut(
                pickup_location=trip.pickup_location,
                drop_location=trip.drop_location,
                date=trip.date,
                seats_available=trip.seats_available,
                price=trip.price,
                ride_fare=trip.ride_fare,
                estimated_time=trip.estimated_time,
                id=trip.id,
                user_id=trip.user_id,
                vehicle_id=trip.vehicle_id,
                status=trip.status,
                is_completed=trip.is_completed,
                is_canceled=trip.is_canceled,
                driver_name=full_name,
                driver_profile_picture=profile_picture,
                vehicle_type=vehicle_type,
                vehicle_image=image_link,
            )
        )
    return results

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


@router.get("/trips/", response_model=list[trip_schemas.TripDetailOut])
def get_all_trips(db: Session = Depends(get_db)):
    trips = trip_crud.get_all_trips(db)
    return trips