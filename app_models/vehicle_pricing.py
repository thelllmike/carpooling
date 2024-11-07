# models/vehicle_pricing.py
from sqlalchemy import Column, Integer, String, Float
from db import Base

class VehiclePricing(Base):
    __tablename__ = "vehicle_pricings"

    id = Column(Integer, primary_key=True, index=True)
    vehicle_type = Column(String, unique=True, index=True, nullable=False)
    rate_per_km = Column(Float, nullable=False)