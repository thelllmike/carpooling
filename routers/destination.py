from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from crud import destination as destination_crud
from schemas import destination as destination_schemas
from db import get_db

router = APIRouter()

@router.post("/destinations/", response_model=destination_schemas.DestinationOut)
def create_destination(destination: destination_schemas.DestinationCreate, db: Session = Depends(get_db)):
    return destination_crud.create_destination(db, destination)

@router.get("/destinations/{destination_id}", response_model=destination_schemas.DestinationOut)
def read_destination(destination_id: int, db: Session = Depends(get_db)):
    db_destination = destination_crud.get_destination(db, destination_id)
    if db_destination is None:
        raise HTTPException(status_code=404, detail="Destination not found")
    return db_destination

@router.get("/destinations/", response_model=list[destination_schemas.DestinationOut])
def read_destinations(db: Session = Depends(get_db)):
    return destination_crud.get_destinations(db)

@router.delete("/destinations/{destination_id}", response_model=destination_schemas.DestinationOut)
def delete_destination(destination_id: int, db: Session = Depends(get_db)):
    db_destination = destination_crud.delete_destination(db, destination_id)
    if db_destination is None:
        raise HTTPException(status_code=404, detail="Destination not found")
    return db_destination
