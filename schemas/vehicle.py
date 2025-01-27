from pydantic import BaseModel

class VehicleBase(BaseModel):
    make: str
    model: str
    license_plate: str
    user_id: int
    image_link: str = None  # Optional field for storing the image link
    available_seat: int  # Number of available seats in the vehicle
    vehicle_type: str  # Type of vehicle (e.g., SUV, Van, Sedan)

class VehicleCreate(VehicleBase):
    pass

class VehicleOut(VehicleBase):
    id: int

    class Config:
        orm_mode = True