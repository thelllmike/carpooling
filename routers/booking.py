from typing import Dict, List
from fastapi import APIRouter, Depends, HTTPException ,Body
from sqlalchemy.orm import Session
from crud import booking as ride_booking_crud
from schemas.booking import RideBookingDetail, RideBookingCreate, RideBookingOut, RideBookingUpdate
from db import get_db

router = APIRouter()

@router.get("/ride_bookings/trip/booking_id/{trip_id}/{user_id}", response_model=Dict[str, int])
def get_booking_id_by_trip_and_user(
    trip_id: int,
    user_id: int,
    db: Session = Depends(get_db)
):
    """
    Given a trip ID and a user ID, find the passenger row (id),
    then find the booking row that references that passenger.id.
    Returns {"booking_id": <int>}.
    """
    booking = ride_booking_crud.get_booking_id_by_trip_and_user(db, trip_id, user_id)
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found for the given trip and user")
    return {"booking_id": booking.id}

@router.get("/trips/{trip_id}", response_model=List[RideBookingDetail])
def get_trip_bookings(trip_id: int, db: Session = Depends(get_db)):
    bookings = ride_booking_crud.get_ride_bookings_by_trip(db, trip_id)
    if not bookings:
        raise HTTPException(status_code=404, detail="No bookings found for this trip")
    return bookings

@router.post("/ride_bookings/", response_model=RideBookingOut)
def create_ride_booking(ride_booking: RideBookingCreate, db: Session = Depends(get_db)):
    return ride_booking_crud.create_ride_booking(db, ride_booking)

@router.get("/ride_bookings/{booking_id}", response_model=RideBookingOut)
def read_ride_booking(booking_id: int, db: Session = Depends(get_db)):
    db_ride_booking = ride_booking_crud.get_ride_booking(db, booking_id)
    if db_ride_booking is None:
        raise HTTPException(status_code=404, detail="Booking not found")
    return db_ride_booking

@router.get("/ride_bookings/trip/{trip_id}", response_model=List[RideBookingOut])
def get_ride_bookings_by_trip(trip_id: int, db: Session = Depends(get_db)):
    bookings = ride_booking_crud.get_ride_bookings_by_trip(db, trip_id)
    if not bookings:
        raise HTTPException(status_code=404, detail="No bookings found for this trip")
    return bookings

# @router.put("/ride_bookings/{booking_id}", response_model=RideBookingOut)
# def update_ride_booking(
#     booking_id: int,
#     confirmed: bool = Body(...),  # Note: we parse 'confirmed' from the JSON body
#     db: Session = Depends(get_db),
# ):
#     db_ride_booking = ride_booking_crud.update_ride_booking(db, booking_id, confirmed)
#     if db_ride_booking is None:
#         raise HTTPException(status_code=404, detail="Booking not found")
#     return db_ride_booking

@router.put("/ride_bookings/{booking_id}", response_model=RideBookingOut)
def update_ride_booking(
    booking_id: int,
    booking_update: RideBookingUpdate,  # now expecting a JSON object
    db: Session = Depends(get_db),
):
    confirmed = booking_update.confirmed
    db_ride_booking = ride_booking_crud.update_ride_booking(db, booking_id, confirmed)
    if db_ride_booking is None:
        raise HTTPException(status_code=404, detail="Booking not found")
    return db_ride_booking
# @router.put("/ride_bookings/{booking_id}", response_model=RideBookingOut)
# def update_ride_booking(booking_id: int, confirmed: bool, db: Session = Depends(get_db)):
#     db_ride_booking = ride_booking_crud.update_ride_booking(db, booking_id, confirmed)
#     if db_ride_booking is None:
#         raise HTTPException(status_code=404, detail="Booking not found")
#     return db_ride_booking

@router.delete("/ride_bookings/{booking_id}", response_model=RideBookingOut)
def delete_ride_booking(booking_id: int, db: Session = Depends(get_db)):
    db_ride_booking = ride_booking_crud.delete_ride_booking(db, booking_id)
    if db_ride_booking is None:
        raise HTTPException(status_code=404, detail="Booking not found")
    return db_ride_booking
