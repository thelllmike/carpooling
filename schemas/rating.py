from pydantic import BaseModel
from typing import Optional

class RatingBase(BaseModel):
    trip_id: int
    rated_by_user_id: int
    driver_id: Optional[int] = None  # New field for driver ID
    rating: int
    feedback: Optional[str] = None  # Optional feedback

class RatingCreate(RatingBase):
    pass

class RatingOut(RatingBase):
    id: int

    class Config:
        orm_mode = True  # Enables ORM compatibility for SQLAlchemy models
