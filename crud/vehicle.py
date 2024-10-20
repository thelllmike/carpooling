from sqlalchemy.orm import Session
from app_models.vehicle import Vehicle
from schemas.vehicle import VehicleCreate

def create_vehicle(db: Session, vehicle: VehicleCreate):
    db_vehicle = Vehicle(**vehicle.dict())
    db.add(db_vehicle)
    db.commit()
    db.refresh(db_vehicle)
    return db_vehicle

def get_vehicle(db: Session, vehicle_id: int):
    return db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()

def get_vehicles_by_user(db: Session, user_id: int):
    return db.query(Vehicle).filter(Vehicle.user_id == user_id).all()

def delete_vehicle(db: Session, vehicle_id: int):
    db_vehicle = get_vehicle(db, vehicle_id)
    if db_vehicle:
        db.delete(db_vehicle)
        db.commit()
    return db_vehicle
