from sqlalchemy.orm import Session
from app_models.destination import Destination
from schemas.destination import DestinationCreate

def create_destination(db: Session, destination: DestinationCreate):
    db_destination = Destination(**destination.dict())
    db.add(db_destination)
    db.commit()
    db.refresh(db_destination)
    return db_destination

def get_destination(db: Session, destination_id: int):
    return db.query(Destination).filter(Destination.id == destination_id).first()

def get_destinations(db: Session):
    return db.query(Destination).all()

def delete_destination(db: Session, destination_id: int):
    db_destination = get_destination(db, destination_id)
    if db_destination:
        db.delete(db_destination)
        db.commit()
    return db_destination
