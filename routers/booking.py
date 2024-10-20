from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from crud import booking as ride_booking_crud
from schemas import booking as ride_booking_schemas
from db import get_db

router = APIRouter()

# Create a new ride booking
@router.post("/ride_bookings/", response_model=ride_booking_schemas.RideBookingOut)
def create_ride_booking(ride_booking: ride_booking_schemas.RideBookingCreate, db: Session = Depends(get_db)):
    return ride_booking_crud.create_ride_booking(db, ride_booking)

# Get a ride booking by ID
@router.get("/ride_bookings/{booking_id}", response_model=ride_booking_schemas.RideBookingOut)
def read_ride_booking(booking_id: int, db: Session = Depends(get_db)):
    db_ride_booking = ride_booking_crud.get_ride_booking(db, booking_id)
    if db_ride_booking is None:
        raise HTTPException(status_code=404, detail="Booking not found")
    return db_ride_booking

# Get ride bookings by trip ID
@router.get("/ride_bookings/trip/{trip_id}", response_model=list[ride_booking_schemas.RideBookingOut])
def get_ride_bookings_by_trip(trip_id: int, db: Session = Depends(get_db)):
    return ride_booking_crud.get_ride_bookings_by_trip(db, trip_id)

# Update ride booking confirmation status
@router.put("/ride_bookings/{booking_id}", response_model=ride_booking_schemas.RideBookingOut)
def update_ride_booking(booking_id: int, confirmed: bool, db: Session = Depends(get_db)):
    db_ride_booking = ride_booking_crud.update_ride_booking(db, booking_id, confirmed)
    if db_ride_booking is None:
        raise HTTPException(status_code=404, detail="Booking not found")
    return db_ride_booking

# Delete a ride booking
@router.delete("/ride_bookings/{booking_id}", response_model=ride_booking_schemas.RideBookingOut)
def delete_ride_booking(booking_id: int, db: Session = Depends(get_db)):
    db_ride_booking = ride_booking_crud.delete_ride_booking(db, booking_id)
    if db_ride_booking is None:
        raise HTTPException(status_code=404, detail="Booking not found")
    return db_ride_booking
