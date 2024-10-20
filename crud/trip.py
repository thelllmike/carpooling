from sqlalchemy.orm import Session
from app_models.trip import Trip
from schemas.trip import TripCreate, TripUpdate

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
