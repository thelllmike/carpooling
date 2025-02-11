from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from crud import start as start_crud
from schemas import start as start_schemas
from db import get_db

router = APIRouter()

@router.post("/starts/", response_model=start_schemas.StartOut)
def create_start(start: start_schemas.StartCreate, db: Session = Depends(get_db)):
    return start_crud.create_start(db, start)

@router.get("/starts/{start_id}", response_model=start_schemas.StartOut)
def read_start(start_id: int, db: Session = Depends(get_db)):
    db_start = start_crud.get_start(db, start_id)
    if db_start is None:
        raise HTTPException(status_code=404, detail="start not found")
    return db_start

@router.get("/starts/", response_model=list[start_schemas.StartOut])
def read_starts(db: Session = Depends(get_db)):
    return start_crud.get_starts(db)

@router.delete("/starts/{start_id}", response_model=start_schemas.StartOut)
def delete_start(start_id: int, db: Session = Depends(get_db)):
    db_start = start_crud.delete_start(db, start_id)
    if db_start is None:
        raise HTTPException(status_code=404, detail="start not found")
    return db_start
