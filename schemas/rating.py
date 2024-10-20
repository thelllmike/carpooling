from pydantic import BaseModel

class RatingBase(BaseModel):
    trip_id: int
    rated_by_user_id: int
    passenger_id: int
    rating: int
    feedback: str

class RatingCreate(RatingBase):
    pass

class RatingOut(RatingBase):
    id: int

    class Config:
        orm_mode = True
