from typing import Optional
from pydantic import BaseModel

class VehicleBase(BaseModel):
    make: str
    model: str
    license_plate: str
    user_id: int
    image_link: str | None = None  # Optional field for storing the image link
    available_seat: int
    vehicle_type: str  # E.g. SUV, Van, Sedan, etc.

class VehicleCreate(VehicleBase):
    pass

class VehicleUpdate(BaseModel):
    make: Optional[str] = None
    model: Optional[str] = None
    license_plate: Optional[str] = None
    user_id: Optional[int] = None
    image_link: Optional[str] = None
    available_seat: Optional[int] = None
    vehicle_type: Optional[str] = None

class VehicleOut(VehicleBase):
    id: int

    class Config:
        orm_mode = True
