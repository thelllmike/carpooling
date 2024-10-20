from sqlalchemy.orm import Session
from app_models.booking import RideBooking
from schemas.booking import RideBookingCreate

# Create a new ride booking
def create_ride_booking(db: Session, ride_booking: RideBookingCreate):
    db_ride_booking = RideBooking(**ride_booking.dict())
    db.add(db_ride_booking)
    db.commit()
    db.refresh(db_ride_booking)
    return db_ride_booking

# Get a ride booking by ID
def get_ride_booking(db: Session, booking_id: int):
    return db.query(RideBooking).filter(RideBooking.id == booking_id).first()

# Get all bookings for a specific trip
def get_ride_bookings_by_trip(db: Session, trip_id: int):
    return db.query(RideBooking).filter(RideBooking.trip_id == trip_id).all()

# Update a ride booking (e.g., confirmation status)
def update_ride_booking(db: Session, booking_id: int, confirmed: bool):
    db_ride_booking = get_ride_booking(db, booking_id)
    if db_ride_booking:
        db_ride_booking.confirmed = confirmed
        db.commit()
        db.refresh(db_ride_booking)
    return db_ride_booking

# Delete a ride booking
def delete_ride_booking(db: Session, booking_id: int):
    db_ride_booking = get_ride_booking(db, booking_id)
    if db_ride_booking:
        db.delete(db_ride_booking)
        db.commit()
    return db_ride_booking
