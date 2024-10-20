from sqlalchemy.orm import Session
from app_models.passenger import Passenger
from schemas.passenger import PassengerCreate

def create_passenger(db: Session, passenger: PassengerCreate):
    db_passenger = Passenger(**passenger.dict())
    db.add(db_passenger)
    db.commit()
    db.refresh(db_passenger)
    return db_passenger

def get_passenger(db: Session, passenger_id: int):
    return db.query(Passenger).filter(Passenger.id == passenger_id).first()

def delete_passenger(db: Session, passenger_id: int):
    db_passenger = get_passenger(db, passenger_id)
    if db_passenger:
        db.delete(db_passenger)
        db.commit()
    return db_passenger
