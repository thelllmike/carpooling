from sqlalchemy.orm import Session
from app_models.rating import Rating
from schemas.rating import RatingCreate

def create_rating(db: Session, rating: RatingCreate):
    db_rating = Rating(**rating.dict())
    db.add(db_rating)
    db.commit()
    db.refresh(db_rating)
    return db_rating

def get_rating(db: Session, rating_id: int):
    return db.query(Rating).filter(Rating.id == rating_id).first()

def get_ratings_by_trip(db: Session, trip_id: int):
    return db.query(Rating).filter(Rating.trip_id == trip_id).all()

def delete_rating(db: Session, rating_id: int):
    db_rating = get_rating(db, rating_id)
    if db_rating:
        db.delete(db_rating)
        db.commit()
    return db_rating
