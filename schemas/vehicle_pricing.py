# schemas/vehicle_pricing.py
from pydantic import BaseModel

class VehiclePricingBase(BaseModel):
    vehicle_type: str
    rate_per_km: float

class VehiclePricingCreate(VehiclePricingBase):
    pass

class VehiclePricingOut(VehiclePricingBase):
    id: int

    class Config:
        orm_mode = True