from pydantic import BaseModel

class VehicleBase(BaseModel):
    make: str
    model: str
    license_plate: str
    user_id: int
    image_link: str = None  # Optional field for storing the image link

class VehicleCreate(VehicleBase):
    pass

class VehicleOut(VehicleBase):
    id: int

    class Config:
        orm_mode = True