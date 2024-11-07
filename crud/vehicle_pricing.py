# crud/vehicle_pricing.py
from sqlalchemy.orm import Session
from app_models.vehicle_pricing import VehiclePricing
from schemas.vehicle_pricing import VehiclePricingCreate

def create_vehicle_pricing(db: Session, vehicle_pricing: VehiclePricingCreate):
    db_vehicle_pricing = VehiclePricing(
        vehicle_type=vehicle_pricing.vehicle_type,
        rate_per_km=vehicle_pricing.rate_per_km
    )
    db.add(db_vehicle_pricing)
    db.commit()
    db.refresh(db_vehicle_pricing)
    return db_vehicle_pricing

def get_vehicle_pricings(db: Session, skip: int = 0, limit: int = 100):
    return db.query(VehiclePricing).offset(skip).limit(limit).all()

def get_vehicle_pricing_by_type(db: Session, vehicle_type: str):
    return db.query(VehiclePricing).filter(VehiclePricing.vehicle_type == vehicle_type).first()