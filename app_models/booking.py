from sqlalchemy import Column, Integer, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from db import Base
from datetime import datetime

class RideBooking(Base):
    __tablename__ = "ride_bookings"
    
    id = Column(Integer, primary_key=True, index=True)
    trip_id = Column(Integer, ForeignKey("trips.id"), nullable=False)
    passenger_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    pickup_location_id = Column(Integer, ForeignKey("destinations.id"), nullable=False)
    drop_location_id = Column(Integer, ForeignKey("destinations.id"), nullable=False)
    confirmed = Column(Boolean, default=False)
    booked_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    # trip = relationship("Trip", back_populates="ride_bookings")
    # passenger = relationship("User", back_populates="ride_bookings")
    # pickup_location = relationship("Destination", foreign_keys=[pickup_location_id])
    # drop_location = relationship("Destination", foreign_keys=[drop_location_id])
