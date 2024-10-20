from pydantic import BaseModel
from datetime import datetime

class PassengerBase(BaseModel):
    user_id: int
    trip_id: int
    status: str = "Pending"

class PassengerCreate(PassengerBase):
    pass

class PassengerOut(PassengerBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
