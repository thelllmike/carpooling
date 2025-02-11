from sqlalchemy.orm import Session
from app_models.start import Start
from schemas.start import StartCreate

def create_start(db: Session, start: StartCreate):
    db_start = Start(**start.dict())
    db.add(db_start)
    db.commit()
    db.refresh(db_start)
    return db_start

def get_start(db: Session, start_id: int):
    return db.query(Start).filter(Start.id == start_id).first()

def get_start(db: Session):
    return db.query(Start).all()

def delete_start(db: Session, start_id: int):
    db_start = get_start(db, start_id)
    if db_start:
        db.delete(db_start)
        db.commit()
    return db_start
