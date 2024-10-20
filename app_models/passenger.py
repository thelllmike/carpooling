from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from db import Base
from datetime import datetime

class Passenger(Base):
    __tablename__ = "passengers"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    trip_id = Column(Integer, ForeignKey("trips.id"), nullable=False)
    status = Column(String(20), default="Pending")  # Pending, Confirmed, Completed, Cancelled
    created_at = Column(DateTime, default=datetime.utcnow)
