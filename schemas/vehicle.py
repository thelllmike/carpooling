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

class VehicleOut(VehicleBase):
    id: int

    class Config:
        orm_mode = True
