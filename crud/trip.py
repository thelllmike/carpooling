from sqlalchemy.orm import Session
from app_models.trip import Trip
from schemas.trip import TripCreate, TripUpdate ,TripDetailOut
from app_models.user import User
from app_models.vehicle import Vehicle

# Create a new trip
def create_trip(db: Session, trip: TripCreate):
    db_trip = Trip(**trip.dict())
    db.add(db_trip)
    db.commit()
    db.refresh(db_trip)
    return db_trip

# Get a trip by ID
def get_trip(db: Session, trip_id: int):
    return db.query(Trip).filter(Trip.id == trip_id).first()

# Get all trips by driver ID
def get_trips_by_driver(db: Session, user_id: int):
    return db.query(Trip).filter(Trip.user_id == user_id).all()

# Update trip (e.g., status, is_completed, is_canceled)
def update_trip(db: Session, trip_id: int, trip_update: TripUpdate):
    db_trip = get_trip(db, trip_id)
    if db_trip:
        for key, value in trip_update.dict(exclude_unset=True).items():
            setattr(db_trip, key, value)
        db.commit()
        db.refresh(db_trip)
    return db_trip

# Delete a trip
def delete_trip(db: Session, trip_id: int):
    db_trip = get_trip(db, trip_id)
    if db_trip:
        db.delete(db_trip)
        db.commit()
    return db_trip


# Get all trips with driver profile picture and vehicle details
def get_all_trips(db: Session):
    trips = (
        db.query(
            Trip,
            User.full_name,
            User.profile_picture,
            Vehicle.vehicle_type,
            Vehicle.image_link,
        )
        .join(User, Trip.user_id == User.id)
        .join(Vehicle, Trip.vehicle_id == Vehicle.id)
        .all()
    )

    return [
        TripDetailOut(
            pickup_location=trip.Trip.pickup_location,
            drop_location=trip.Trip.drop_location,
            date=trip.Trip.date,
            seats_available=trip.Trip.seats_available,
            price=trip.Trip.price,
            ride_fare=trip.Trip.ride_fare,
            estimated_time=trip.Trip.estimated_time,
            id=trip.Trip.id,
            user_id=trip.Trip.user_id,
            vehicle_id=trip.Trip.vehicle_id,
            status=trip.Trip.status,
            is_completed=trip.Trip.is_completed,
            is_canceled=trip.Trip.is_canceled,
            driver_name=trip.full_name,
            driver_profile_picture=trip.profile_picture,
            vehicle_type=trip.vehicle_type,
            vehicle_image=trip.image_link,
        )
        for trip in trips
    ]

def update_seat_availability(db: Session, trip_id: int, seats_available: int):
    db_trip = get_trip(db, trip_id)
    if db_trip:
        db_trip.seats_available = seats_available
        db.commit()
        db.refresh(db_trip)
    return db_trip
