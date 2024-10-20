from pydantic import BaseModel

class VehicleBase(BaseModel):
    make: str
    model: str
    license_plate: str
    user_id: int

class VehicleCreate(VehicleBase):
    pass

class VehicleOut(VehicleBase):
    id: int

    class Config:
        orm_mode = True
