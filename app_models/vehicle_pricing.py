from sqlalchemy import Column, Integer, String, Float
from db import Base

class VehiclePricing(Base):
    __tablename__ = "vehicle_pricings"

    id = Column(Integer, primary_key=True, index=True)
    vehicle_type = Column(String(50), unique=True, index=True, nullable=False)  # Added length for VARCHAR
    rate_per_km = Column(Float, nullable=False)
