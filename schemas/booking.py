from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class RideBookingBase(BaseModel):
    trip_id: int
    passenger_id: int
    pickup_location_id: int
    drop_location_id: int
    confirmed: Optional[bool] = False

class RideBookingCreate(RideBookingBase):
    pass

class RideBookingOut(RideBookingBase):
    id: int
    booked_at: datetime

    class Config:
        orm_mode = True
