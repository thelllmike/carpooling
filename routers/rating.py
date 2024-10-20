from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from crud import rating as rating_crud
from schemas import rating as rating_schemas
from db import get_db

router = APIRouter()

@router.post("/ratings/", response_model=rating_schemas.RatingOut)
def create_rating(rating: rating_schemas.RatingCreate, db: Session = Depends(get_db)):
    return rating_crud.create_rating(db, rating)

@router.get("/ratings/{rating_id}", response_model=rating_schemas.RatingOut)
def read_rating(rating_id: int, db: Session = Depends(get_db)):
    db_rating = rating_crud.get_rating(db, rating_id)
    if db_rating is None:
        raise HTTPException(status_code=404, detail="Rating not found")
    return db_rating

@router.delete("/ratings/{rating_id}", response_model=rating_schemas.RatingOut)
def delete_rating(rating_id: int, db: Session = Depends(get_db)):
    db_rating = rating_crud.delete_rating(db, rating_id)
    if db_rating is None:
        raise HTTPException(status_code=404, detail="Rating not found")
    return db_rating
